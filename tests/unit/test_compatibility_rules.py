"""Behavior tests for deterministic Day 4 pre-execution filtering."""

import json
from copy import deepcopy
from pathlib import Path

import pytest
from llmopt_optimizer import CandidateCompatibilityEvaluator
from llmopt_schemas import (
    CandidateFilterInput,
    CandidateFilterResult,
    CompatibilityReasonCode,
    CompatibilityRuleId,
    EngineCapabilityRecord,
    ModelTopology,
    RuleCategory,
    RuleDecision,
)

FIXTURES = Path(__file__).parents[1] / "fixtures" / "compatibility" / "v1"


def _load(name: str) -> dict[str, object]:
    value: object = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _merge(base: dict[str, object], patch: dict[str, object]) -> dict[str, object]:
    merged = deepcopy(base)
    for key, value in patch.items():
        current = merged.get(key)
        if isinstance(current, dict) and isinstance(value, dict):
            merged[key] = _merge(current, value)
        else:
            merged[key] = deepcopy(value)
    return merged


@pytest.fixture
def capabilities() -> EngineCapabilityRecord:
    return EngineCapabilityRecord.model_validate(_load("engine-capability.json"))


@pytest.fixture
def allowed_input() -> CandidateFilterInput:
    return CandidateFilterInput.model_validate(_load("allowed-candidate.json"))


def _evaluate(
    input_: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> CandidateFilterResult:
    return CandidateCompatibilityEvaluator().evaluate(input_, capabilities)


@pytest.mark.unit
def test_allowed_candidate_passes_every_rule(
    allowed_input: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> None:
    result = _evaluate(allowed_input, capabilities)

    assert result.decision is RuleDecision.ALLOWED
    assert result.engine_compatibility is RuleDecision.ALLOWED
    assert result.orionix_certification is RuleDecision.ALLOWED
    assert len(result.rule_results) == 13
    assert all(item.decision is RuleDecision.ALLOWED for item in result.rule_results)


@pytest.mark.unit
def test_required_example_cases_return_expected_public_decisions(
    capabilities: EngineCapabilityRecord,
) -> None:
    base = _load("allowed-candidate.json")
    suite = _load("example-cases.json")
    cases = suite["cases"]
    assert isinstance(cases, list)

    for raw_case in cases:
        assert isinstance(raw_case, dict)
        patch = raw_case["patch"]
        assert isinstance(patch, dict)
        input_ = CandidateFilterInput.model_validate(_merge(base, patch))
        result = _evaluate(input_, capabilities)
        assert result.decision.value == raw_case["expected_decision"], raw_case["name"]
        assert raw_case["expected_reason_code"] in {
            item.reason_code.value for item in result.rule_results
        }, raw_case["name"]


@pytest.mark.unit
def test_engine_compatible_and_certified_are_independent(
    allowed_input: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> None:
    model = allowed_input.model.model_copy(
        update={"architecture": "UncertifiedSyntheticForCausalLM"}
    )
    input_ = allowed_input.model_copy(update={"model": model})

    result = _evaluate(input_, capabilities)

    assert result.engine_compatibility is RuleDecision.ALLOWED
    assert result.orionix_certification is RuleDecision.EXPERIMENTAL
    assert result.decision is RuleDecision.EXPERIMENTAL
    certification = next(
        item for item in result.rule_results if item.category is RuleCategory.ORIONIX_CERTIFICATION
    )
    assert certification.reason_code is CompatibilityReasonCode.ENGINE_COMPATIBLE_NOT_CERTIFIED


@pytest.mark.unit
def test_multiple_rejections_are_returned_in_deterministic_order(
    allowed_input: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> None:
    model = allowed_input.model.model_copy(update={"quantization": "gptq"})
    config = allowed_input.candidate.configuration.model_copy(
        update={
            "precision": "float8_e4m3fn",
            "parallelism": allowed_input.candidate.configuration.parallelism.model_copy(
                update={"tp": 4, "ep": 2}
            ),
        }
    )
    candidate = allowed_input.candidate.model_copy(update={"configuration": config})
    input_ = allowed_input.model_copy(update={"model": model, "candidate": candidate})

    first = _evaluate(input_, capabilities)
    second = _evaluate(input_, capabilities)

    assert first == second
    assert first.decision is RuleDecision.REJECTED
    rejected_codes = {
        item.reason_code for item in first.rule_results if item.decision is RuleDecision.REJECTED
    }
    assert CompatibilityReasonCode.UNSUPPORTED_PRECISION in rejected_codes
    assert CompatibilityReasonCode.UNSUPPORTED_QUANTIZATION in rejected_codes
    assert CompatibilityReasonCode.INVALID_TENSOR_PARALLEL_SIZE in rejected_codes
    assert CompatibilityReasonCode.EXPERT_PARALLELISM_REQUIRES_MOE in rejected_codes


@pytest.mark.unit
def test_missing_estimates_never_become_automatic_approval(
    allowed_input: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> None:
    input_ = allowed_input.model_copy(update={"memory_estimate": None, "execution_estimate": None})

    result = _evaluate(input_, capabilities)

    assert result.decision is RuleDecision.EXPERIMENTAL
    experimental_rules = {
        item.rule_id for item in result.rule_results if item.decision is RuleDecision.EXPERIMENTAL
    }
    assert CompatibilityRuleId.GPU_MEMORY in experimental_rules
    assert CompatibilityRuleId.TIME_BUDGET in experimental_rules
    assert CompatibilityRuleId.COST_BUDGET in experimental_rules


@pytest.mark.unit
def test_context_above_engine_limit_is_rejected(
    allowed_input: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> None:
    input_ = allowed_input.model_copy(update={"requested_context_length": 65536})

    result = _evaluate(input_, capabilities)

    context = next(
        item for item in result.rule_results if item.rule_id is CompatibilityRuleId.CONTEXT_LENGTH
    )
    assert context.decision is RuleDecision.REJECTED
    assert context.reason_code is CompatibilityReasonCode.CONTEXT_LENGTH_EXCEEDS_ENGINE_LIMIT


@pytest.mark.unit
def test_dense_model_with_expert_parallelism_is_rejected(
    allowed_input: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> None:
    parallelism = allowed_input.candidate.configuration.parallelism.model_copy(update={"ep": 2})
    config = allowed_input.candidate.configuration.model_copy(update={"parallelism": parallelism})
    candidate = allowed_input.candidate.model_copy(update={"configuration": config})

    result = _evaluate(allowed_input.model_copy(update={"candidate": candidate}), capabilities)

    expert = next(
        item
        for item in result.rule_results
        if item.rule_id is CompatibilityRuleId.EXPERT_PARALLELISM
    )
    assert allowed_input.model.dense_or_moe is ModelTopology.DENSE
    assert expert.reason_code is CompatibilityReasonCode.EXPERT_PARALLELISM_REQUIRES_MOE


@pytest.mark.unit
def test_explicit_topology_mismatch_is_rejected(
    allowed_input: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> None:
    link = allowed_input.hardware.cluster.interconnects[0].model_copy(
        update={"peer_access_capable": False}
    )
    cluster = allowed_input.hardware.cluster.model_copy(update={"interconnects": (link,)})
    hardware = allowed_input.hardware.model_copy(update={"cluster": cluster})

    result = _evaluate(allowed_input.model_copy(update={"hardware": hardware}), capabilities)

    topology = next(
        item
        for item in result.rule_results
        if item.rule_id is CompatibilityRuleId.PARALLELISM_TOPOLOGY
    )
    assert topology.decision is RuleDecision.REJECTED
    assert topology.reason_code is CompatibilityReasonCode.PARALLELISM_TOPOLOGY_MISMATCH


@pytest.mark.unit
@pytest.mark.parametrize(
    ("field", "value", "reason"),
    (
        ("elapsed_seconds", 7200.0, CompatibilityReasonCode.TIME_BUDGET_EXCEEDED),
        ("gpu_hours", 5.0, CompatibilityReasonCode.COST_BUDGET_EXCEEDED),
        ("cost_usd", 50.0, CompatibilityReasonCode.COST_BUDGET_EXCEEDED),
    ),
)
def test_supplied_budget_violations_are_rejected(
    allowed_input: CandidateFilterInput,
    capabilities: EngineCapabilityRecord,
    field: str,
    value: float,
    reason: CompatibilityReasonCode,
) -> None:
    assert allowed_input.execution_estimate is not None
    estimate = allowed_input.execution_estimate.model_copy(update={field: value})

    result = _evaluate(
        allowed_input.model_copy(update={"execution_estimate": estimate}), capabilities
    )

    assert reason in {
        item.reason_code for item in result.rule_results if item.decision is RuleDecision.REJECTED
    }


@pytest.mark.unit
def test_unknown_future_architecture_is_experimental_not_certified(
    allowed_input: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> None:
    nodes = []
    for node in allowed_input.hardware.cluster.nodes:
        accelerators = tuple(
            accelerator.model_copy(update={"architecture_family": "future-architecture-x"})
            for accelerator in node.accelerators
        )
        nodes.append(node.model_copy(update={"accelerators": accelerators}))
    cluster = allowed_input.hardware.cluster.model_copy(update={"nodes": tuple(nodes)})
    hardware = allowed_input.hardware.model_copy(update={"cluster": cluster})

    result = _evaluate(allowed_input.model_copy(update={"hardware": hardware}), capabilities)

    architecture = next(
        item for item in result.rule_results if item.rule_id is CompatibilityRuleId.GPU_ARCHITECTURE
    )
    assert architecture.decision is RuleDecision.EXPERIMENTAL
    assert architecture.reason_code is CompatibilityReasonCode.UNKNOWN_GPU_ARCHITECTURE
    assert result.orionix_certification is RuleDecision.EXPERIMENTAL


@pytest.mark.unit
def test_result_serialization_is_stable_and_input_is_not_mutated(
    allowed_input: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> None:
    before = allowed_input.model_dump_json()

    result = _evaluate(allowed_input, capabilities)
    restored = CandidateFilterResult.model_validate_json(result.model_dump_json())

    assert restored == result
    assert allowed_input.model_dump_json() == before


@pytest.mark.unit
def test_customer_messages_do_not_include_sensitive_internal_details(
    allowed_input: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> None:
    result = _evaluate(allowed_input, capabilities)
    rendered = " ".join(
        f"{item.message} {item.remediation or ''}" for item in result.rule_results
    ).casefold()

    assert "traceback" not in rendered
    assert "/users/" not in rendered
    assert "sha256:" not in rendered
    assert "password" not in rendered
    assert "secret" not in rendered

"""Golden JSON examples freeze the first shared cross-component contracts."""

import json
from pathlib import Path

import pytest
from llmopt_capsule import ExecutionCapsuleManifest
from llmopt_schemas import (
    AcceleratorSpec,
    BenchmarkResult,
    CandidateConfiguration,
    ClusterSpec,
    HardwareSpec,
    ModelSpec,
    NodeSpec,
    OptimizationJobSpec,
    OptimizationRequirements,
    Recommendation,
    SoftwareEnvironmentSpec,
    WorkloadSpec,
)
from llmopt_schemas.base import ContractModel
from pydantic import ValidationError

FIXTURES = Path(__file__).parents[1] / "fixtures" / "contracts" / "v1"

GOLDEN_CONTRACTS: dict[str, type[ContractModel]] = {
    "accelerator.json": AcceleratorSpec,
    "node.json": NodeSpec,
    "cluster.json": ClusterSpec,
    "software-environment.json": SoftwareEnvironmentSpec,
    "hardware.json": HardwareSpec,
    "model.json": ModelSpec,
    "workload.json": WorkloadSpec,
    "requirements.json": OptimizationRequirements,
    "optimization-job.json": OptimizationJobSpec,
    "candidate-configuration.json": CandidateConfiguration,
    "benchmark-result.json": BenchmarkResult,
    "recommendation.json": Recommendation,
    "execution-capsule.json": ExecutionCapsuleManifest,
}


def _payload(name: str) -> dict[str, object]:
    loaded: object = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


@pytest.mark.contract
@pytest.mark.parametrize(("fixture_name", "contract"), GOLDEN_CONTRACTS.items())
def test_golden_contract_round_trip(fixture_name: str, contract: type[ContractModel]) -> None:
    parsed = contract.model_validate(_payload(fixture_name))

    restored = contract.model_validate_json(parsed.model_dump_json())

    assert restored == parsed
    assert getattr(restored, "schema_version") == getattr(  # noqa: B009
        contract, "SCHEMA_VERSION"
    )


@pytest.mark.contract
@pytest.mark.parametrize(("fixture_name", "contract"), GOLDEN_CONTRACTS.items())
def test_saved_contract_rejects_missing_schema_version(
    fixture_name: str, contract: type[ContractModel]
) -> None:
    payload = _payload(fixture_name)
    payload.pop("schema_version")

    with pytest.raises(ValidationError, match="explicit schema_version"):
        contract.model_validate(payload)


@pytest.mark.contract
@pytest.mark.parametrize(("fixture_name", "contract"), GOLDEN_CONTRACTS.items())
def test_saved_contract_rejects_an_older_schema_version(
    fixture_name: str, contract: type[ContractModel]
) -> None:
    payload = _payload(fixture_name)
    payload["schema_version"] = "0.9"

    with pytest.raises(ValidationError, match="supports schema_version"):
        contract.model_validate(payload)


@pytest.mark.contract
def test_accelerator_rejects_negative_memory() -> None:
    payload = _payload("accelerator.json")
    payload["vram_bytes"] = -1

    with pytest.raises(ValidationError):
        AcceleratorSpec.model_validate(payload)


@pytest.mark.contract
def test_unknown_future_architecture_is_representable_without_support_claim() -> None:
    accelerator = AcceleratorSpec.model_validate(_payload("accelerator.json"))

    assert accelerator.architecture_family == "future_architecture_x"
    assert "support" not in AcceleratorSpec.model_fields
    assert "certified" not in AcceleratorSpec.model_fields

"""Deterministic, CPU-only pre-execution compatibility filtering."""

from collections.abc import Callable, Iterable
from math import ceil

from llmopt_schemas import (
    AcceleratorEngineCapability,
    AcceleratorSpec,
    CandidateFilterInput,
    CandidateFilterResult,
    CapabilityValues,
    CompatibilityReasonCode,
    CompatibilityRuleId,
    EngineCapabilityRecord,
    ModelTopology,
    RuleCategory,
    RuleDecision,
    RuleResult,
)

RULE_VERSION = "1.0"

Rule = Callable[[CandidateFilterInput, EngineCapabilityRecord], RuleResult]


def _result(
    capabilities: EngineCapabilityRecord,
    rule_id: CompatibilityRuleId,
    decision: RuleDecision,
    reason_code: CompatibilityReasonCode,
    category: RuleCategory,
    message: str,
    remediation: str | None = None,
    **evidence: str | int | float | bool | None,
) -> RuleResult:
    return RuleResult(
        schema_version=RuleResult.SCHEMA_VERSION,
        rule_id=rule_id,
        decision=decision,
        reason_code=reason_code,
        category=category,
        message=message,
        remediation=remediation,
        evidence=evidence,
        capability_record_version=capabilities.record_version,
        rule_version=RULE_VERSION,
    )


def _normalized(value: str) -> str:
    return value.strip().casefold().replace("_", "-")


def _capability_state(values: CapabilityValues, value: str) -> RuleDecision:
    requested = _normalized(value)
    if requested in {_normalized(item) for item in values.supported}:
        return RuleDecision.ALLOWED
    if requested in {_normalized(item) for item in values.unsupported}:
        return RuleDecision.REJECTED
    return RuleDecision.EXPERIMENTAL


def _accelerators(input_: CandidateFilterInput) -> tuple[AcceleratorSpec, ...]:
    return tuple(
        accelerator for node in input_.hardware.cluster.nodes for accelerator in node.accelerators
    )


def _candidate_accelerators(input_: CandidateFilterInput) -> tuple[AcceleratorSpec, ...]:
    accelerators = _accelerators(input_)
    selected = set(input_.placement.accelerator_identifier_hashes)
    if not selected:
        return accelerators
    return tuple(
        accelerator
        for accelerator in accelerators
        if accelerator.device_identifier_hash in selected
    )


def _architecture_row(
    capabilities: EngineCapabilityRecord, vendor: str, architecture: str
) -> AcceleratorEngineCapability | None:
    for row in capabilities.accelerator_capabilities:
        if _normalized(row.vendor) == _normalized(vendor) and _normalized(
            row.architecture_family
        ) == _normalized(architecture):
            return row
    return None


def evaluate_gpu_memory(
    input_: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> RuleResult:
    estimate = input_.memory_estimate
    selected = set(input_.placement.accelerator_identifier_hashes)
    if estimate is None or not selected:
        return _result(
            capabilities,
            CompatibilityRuleId.GPU_MEMORY,
            RuleDecision.EXPERIMENTAL,
            CompatibilityReasonCode.INFORMATION_REQUIRED,
            RuleCategory.RESOURCE,
            "A supplied memory estimate and accelerator placement are required.",
            "Provide estimated model, KV-cache, runtime, and placement memory data.",
        )

    accelerators = [
        accelerator
        for accelerator in _accelerators(input_)
        if accelerator.device_identifier_hash in selected
    ]
    if len(accelerators) != len(selected):
        return _result(
            capabilities,
            CompatibilityRuleId.GPU_MEMORY,
            RuleDecision.EXPERIMENTAL,
            CompatibilityReasonCode.INFORMATION_REQUIRED,
            RuleCategory.RESOURCE,
            "Memory cannot be checked because the placement references unknown accelerators.",
            "Refresh the supplied hardware snapshot and candidate placement.",
        )

    base_required = estimate.model_bytes + estimate.kv_cache_bytes + estimate.runtime_overhead_bytes
    required = ceil(base_required * (1 + estimate.safety_margin_ratio))
    utilization = input_.candidate.configuration.memory.gpu_memory_utilization_ratio or 1.0
    available = sum(int(accelerator.vram_bytes * utilization) for accelerator in accelerators)
    if required > available:
        return _result(
            capabilities,
            CompatibilityRuleId.GPU_MEMORY,
            RuleDecision.REJECTED,
            CompatibilityReasonCode.INSUFFICIENT_GPU_MEMORY,
            RuleCategory.RESOURCE,
            "Estimated model and cache memory exceed available GPU memory.",
            "Use larger GPUs, lower context or concurrency, or a supported lower precision.",
            estimated_required_bytes=required,
            usable_gpu_memory_bytes=available,
            estimate_is_measured=False,
        )
    return _result(
        capabilities,
        CompatibilityRuleId.GPU_MEMORY,
        RuleDecision.ALLOWED,
        CompatibilityReasonCode.CHECK_PASSED,
        RuleCategory.RESOURCE,
        "The supplied memory estimate fits within the selected GPU memory.",
        estimated_required_bytes=required,
        usable_gpu_memory_bytes=available,
        estimate_is_measured=False,
    )


def evaluate_gpu_architecture(
    input_: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> RuleResult:
    accelerators = _candidate_accelerators(input_)
    if not accelerators:
        return _result(
            capabilities,
            CompatibilityRuleId.GPU_ARCHITECTURE,
            RuleDecision.EXPERIMENTAL,
            CompatibilityReasonCode.INFORMATION_REQUIRED,
            RuleCategory.ENGINE_COMPATIBILITY,
            "No accelerator architecture was supplied for compatibility evaluation.",
            "Provide a normalized GPU hardware snapshot.",
        )

    unsupported = {_normalized(item) for item in capabilities.explicitly_unsupported_architectures}
    for accelerator in accelerators:
        architecture = accelerator.architecture_family
        if _normalized(architecture) in unsupported:
            return _result(
                capabilities,
                CompatibilityRuleId.GPU_ARCHITECTURE,
                RuleDecision.REJECTED,
                CompatibilityReasonCode.UNSUPPORTED_GPU_ARCHITECTURE,
                RuleCategory.ENGINE_COMPATIBILITY,
                "The supplied GPU architecture is explicitly unsupported by this engine record.",
                "Choose a supported architecture or a different verified engine record.",
                architecture=architecture,
            )
        if _architecture_row(capabilities, accelerator.vendor, architecture) is None:
            return _result(
                capabilities,
                CompatibilityRuleId.GPU_ARCHITECTURE,
                RuleDecision.EXPERIMENTAL,
                CompatibilityReasonCode.UNKNOWN_GPU_ARCHITECTURE,
                RuleCategory.ENGINE_COMPATIBILITY,
                "The supplied GPU architecture has not been verified for this engine record.",
                "Validate this architecture before spending GPU time.",
                architecture=architecture,
            )
    return _result(
        capabilities,
        CompatibilityRuleId.GPU_ARCHITECTURE,
        RuleDecision.ALLOWED,
        CompatibilityReasonCode.CHECK_PASSED,
        RuleCategory.ENGINE_COMPATIBILITY,
        "All supplied GPU architectures are supported by the engine capability record.",
        accelerator_count=len(accelerators),
    )


def _evaluate_format(
    input_: CandidateFilterInput,
    capabilities: EngineCapabilityRecord,
    value: str,
    *,
    precision: bool,
) -> RuleResult:
    rule_id = CompatibilityRuleId.PRECISION if precision else CompatibilityRuleId.QUANTIZATION
    unsupported_code = (
        CompatibilityReasonCode.UNSUPPORTED_PRECISION
        if precision
        else CompatibilityReasonCode.UNSUPPORTED_QUANTIZATION
    )
    unknown_code = (
        CompatibilityReasonCode.UNKNOWN_PRECISION_SUPPORT
        if precision
        else CompatibilityReasonCode.UNKNOWN_QUANTIZATION_SUPPORT
    )
    label = "precision" if precision else "quantization"
    accelerators = _candidate_accelerators(input_)
    if not accelerators:
        return _result(
            capabilities,
            rule_id,
            RuleDecision.EXPERIMENTAL,
            unknown_code,
            RuleCategory.ENGINE_COMPATIBILITY,
            f"{label.title()} support cannot be established without accelerator data.",
            "Provide accelerator architecture and numeric-format information.",
            requested_value=value,
        )

    for accelerator in accelerators:
        if precision and _normalized(value) not in {
            _normalized(item) for item in accelerator.supported_numeric_formats
        }:
            return _result(
                capabilities,
                rule_id,
                RuleDecision.REJECTED,
                unsupported_code,
                RuleCategory.ENGINE_COMPATIBILITY,
                f"The requested {label} is not supported by the supplied accelerator facts.",
                "Choose a supported format or verified compatible hardware.",
                requested_value=value,
                architecture=accelerator.architecture_family,
            )
        row = _architecture_row(
            capabilities,
            accelerator.vendor,
            accelerator.architecture_family,
        )
        if row is None:
            return _result(
                capabilities,
                rule_id,
                RuleDecision.EXPERIMENTAL,
                unknown_code,
                RuleCategory.ENGINE_COMPATIBILITY,
                f"{label.title()} support is unverified for the supplied GPU architecture.",
                "Validate this combination before execution.",
                requested_value=value,
            )
        values = row.precisions if precision else row.quantizations
        state = _capability_state(values, value)
        if state is RuleDecision.REJECTED:
            return _result(
                capabilities,
                rule_id,
                state,
                unsupported_code,
                RuleCategory.ENGINE_COMPATIBILITY,
                f"The requested {label} is explicitly unsupported for this GPU architecture.",
                "Choose a supported format or a different verified accelerator.",
                requested_value=value,
                architecture=accelerator.architecture_family,
            )
        if state is RuleDecision.EXPERIMENTAL:
            return _result(
                capabilities,
                rule_id,
                state,
                unknown_code,
                RuleCategory.ENGINE_COMPATIBILITY,
                f"The requested {label} has not been verified for this GPU architecture.",
                "Validate this combination before execution.",
                requested_value=value,
                architecture=accelerator.architecture_family,
            )
    return _result(
        capabilities,
        rule_id,
        RuleDecision.ALLOWED,
        CompatibilityReasonCode.CHECK_PASSED,
        RuleCategory.ENGINE_COMPATIBILITY,
        f"The requested {label} is supported by the supplied engine and accelerator facts.",
        requested_value=value,
    )


def evaluate_precision(
    input_: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> RuleResult:
    requested = input_.candidate.configuration.precision or input_.model.dtype
    return _evaluate_format(input_, capabilities, requested, precision=True)


def evaluate_quantization(
    input_: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> RuleResult:
    if input_.model.quantization is None:
        return _result(
            capabilities,
            CompatibilityRuleId.QUANTIZATION,
            RuleDecision.ALLOWED,
            CompatibilityReasonCode.CHECK_PASSED,
            RuleCategory.ENGINE_COMPATIBILITY,
            "No quantization method was requested.",
        )
    return _evaluate_format(input_, capabilities, input_.model.quantization, precision=False)


def evaluate_context_length(
    input_: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> RuleResult:
    limit = capabilities.maximum_context_length
    if limit is None:
        return _result(
            capabilities,
            CompatibilityRuleId.CONTEXT_LENGTH,
            RuleDecision.EXPERIMENTAL,
            CompatibilityReasonCode.ENGINE_CONTEXT_LIMIT_UNKNOWN,
            RuleCategory.ENGINE_COMPATIBILITY,
            "The engine context limit is unknown in this capability record.",
            "Verify the engine limit before execution.",
            requested_context_tokens=input_.requested_context_length,
        )
    if input_.requested_context_length > limit:
        return _result(
            capabilities,
            CompatibilityRuleId.CONTEXT_LENGTH,
            RuleDecision.REJECTED,
            CompatibilityReasonCode.CONTEXT_LENGTH_EXCEEDS_ENGINE_LIMIT,
            RuleCategory.ENGINE_COMPATIBILITY,
            "The requested context length exceeds the pinned engine limit.",
            (
                "Reduce the requested context length or select a verified engine profile "
                "with a higher limit."
            ),
            requested_context_tokens=input_.requested_context_length,
            engine_limit_tokens=limit,
        )
    return _result(
        capabilities,
        CompatibilityRuleId.CONTEXT_LENGTH,
        RuleDecision.ALLOWED,
        CompatibilityReasonCode.CHECK_PASSED,
        RuleCategory.ENGINE_COMPATIBILITY,
        "The requested context length is within the pinned engine limit.",
        requested_context_tokens=input_.requested_context_length,
        engine_limit_tokens=limit,
    )


def evaluate_tensor_parallel_size(
    input_: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> RuleResult:
    parallelism = input_.candidate.configuration.parallelism
    required_devices = parallelism.dp * parallelism.tp * parallelism.pp
    available_devices = input_.hardware.cluster.accelerator_count
    selected = input_.placement.accelerator_identifier_hashes
    constraints = input_.parallelism_constraints
    invalid = (
        required_devices > available_devices
        or len(selected) != len(set(selected))
        or (bool(selected) and len(selected) != required_devices)
        or (
            capabilities.maximum_tensor_parallel_size is not None
            and parallelism.tp > capabilities.maximum_tensor_parallel_size
        )
        or (
            constraints.tensor_parallel_divisor is not None
            and constraints.tensor_parallel_divisor % parallelism.tp != 0
        )
        or (
            constraints.pipeline_parallel_divisor is not None
            and constraints.pipeline_parallel_divisor % parallelism.pp != 0
        )
    )
    if invalid:
        return _result(
            capabilities,
            CompatibilityRuleId.TENSOR_PARALLEL_SIZE,
            RuleDecision.REJECTED,
            CompatibilityReasonCode.INVALID_TENSOR_PARALLEL_SIZE,
            RuleCategory.ENGINE_COMPATIBILITY,
            "The requested parallelism size does not match available or supplied constraints.",
            "Use a GPU count and parallel size supported by the model, engine, and cluster.",
            tensor_parallel_size=parallelism.tp,
            required_accelerators=required_devices,
            available_accelerators=available_devices,
        )
    if not selected:
        return _result(
            capabilities,
            CompatibilityRuleId.TENSOR_PARALLEL_SIZE,
            RuleDecision.EXPERIMENTAL,
            CompatibilityReasonCode.INFORMATION_REQUIRED,
            RuleCategory.ENGINE_COMPATIBILITY,
            "The accelerator placement required to validate parallelism was not supplied.",
            "Supply one unique accelerator placement for every required rank.",
            required_accelerators=required_devices,
        )
    return _result(
        capabilities,
        CompatibilityRuleId.TENSOR_PARALLEL_SIZE,
        RuleDecision.ALLOWED,
        CompatibilityReasonCode.CHECK_PASSED,
        RuleCategory.ENGINE_COMPATIBILITY,
        "The requested parallelism size matches the supplied resources and constraints.",
        tensor_parallel_size=parallelism.tp,
        required_accelerators=required_devices,
    )


def _selected_nodes(input_: CandidateFilterInput) -> dict[str, str]:
    return {
        accelerator.device_identifier_hash: node.node_id
        for node in input_.hardware.cluster.nodes
        for accelerator in node.accelerators
        if accelerator.device_identifier_hash in input_.placement.accelerator_identifier_hashes
    }


def _peer_state(input_: CandidateFilterInput, left: str, right: str) -> bool | None:
    for link in input_.hardware.cluster.interconnects:
        endpoints = {
            link.endpoint_a.accelerator_identifier_hash,
            link.endpoint_b.accelerator_identifier_hash,
        }
        if endpoints == {left, right}:
            return link.peer_access_capable
    return None


def evaluate_parallelism_topology(
    input_: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> RuleResult:
    selected = input_.placement.accelerator_identifier_hashes
    if not selected:
        return _result(
            capabilities,
            CompatibilityRuleId.PARALLELISM_TOPOLOGY,
            RuleDecision.EXPERIMENTAL,
            CompatibilityReasonCode.TOPOLOGY_INFORMATION_REQUIRED,
            RuleCategory.TOPOLOGY,
            "Topology compatibility cannot be checked without an accelerator placement.",
            "Supply the candidate rank placement and interconnect observations.",
        )
    nodes_by_device = _selected_nodes(input_)
    if len(nodes_by_device) != len(set(selected)):
        return _result(
            capabilities,
            CompatibilityRuleId.PARALLELISM_TOPOLOGY,
            RuleDecision.REJECTED,
            CompatibilityReasonCode.PARALLELISM_TOPOLOGY_MISMATCH,
            RuleCategory.TOPOLOGY,
            "The candidate placement references accelerators outside the supplied cluster.",
            "Refresh the cluster snapshot and choose accelerators that exist in it.",
        )
    selected_nodes = set(nodes_by_device.values())
    supplied_nodes = input_.placement.node_ids
    derived_nodes = tuple(nodes_by_device[device] for device in selected)
    if supplied_nodes and supplied_nodes != derived_nodes:
        return _result(
            capabilities,
            CompatibilityRuleId.PARALLELISM_TOPOLOGY,
            RuleDecision.REJECTED,
            CompatibilityReasonCode.PARALLELISM_TOPOLOGY_MISMATCH,
            RuleCategory.TOPOLOGY,
            "The supplied node placement does not match the selected accelerators.",
            "Refresh the placement so every selected accelerator maps to its actual node.",
        )
    if input_.parallelism_constraints.single_node_only and len(selected_nodes) > 1:
        return _result(
            capabilities,
            CompatibilityRuleId.PARALLELISM_TOPOLOGY,
            RuleDecision.REJECTED,
            CompatibilityReasonCode.PARALLELISM_TOPOLOGY_MISMATCH,
            RuleCategory.TOPOLOGY,
            "A single-node candidate cannot place ranks across multiple nodes.",
            "Place all ranks on one node or use a verified multi-node plan.",
            selected_node_count=len(selected_nodes),
        )
    require_peer = (
        input_.parallelism_constraints.require_peer_access
        or input_.candidate.configuration.parallelism.tp > 1
    )
    if require_peer and len(selected) > 1:
        states = [
            _peer_state(input_, selected[index], selected[other])
            for index in range(len(selected))
            for other in range(index + 1, len(selected))
        ]
        if any(state is False for state in states):
            return _result(
                capabilities,
                CompatibilityRuleId.PARALLELISM_TOPOLOGY,
                RuleDecision.REJECTED,
                CompatibilityReasonCode.PARALLELISM_TOPOLOGY_MISMATCH,
                RuleCategory.TOPOLOGY,
                "The selected GPUs do not provide required peer access.",
                "Choose a peer-connected placement or reduce tensor parallelism.",
            )
        if any(state is None for state in states):
            return _result(
                capabilities,
                CompatibilityRuleId.PARALLELISM_TOPOLOGY,
                RuleDecision.EXPERIMENTAL,
                CompatibilityReasonCode.TOPOLOGY_INFORMATION_REQUIRED,
                RuleCategory.TOPOLOGY,
                "Required peer-access topology information is incomplete.",
                "Supply peer-access observations for the selected GPUs.",
            )
    return _result(
        capabilities,
        CompatibilityRuleId.PARALLELISM_TOPOLOGY,
        RuleDecision.ALLOWED,
        CompatibilityReasonCode.CHECK_PASSED,
        RuleCategory.TOPOLOGY,
        "The supplied accelerator placement matches the topology constraints.",
        selected_node_count=len(selected_nodes),
    )


def evaluate_time_budget(
    input_: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> RuleResult:
    estimate = input_.execution_estimate
    maximum = input_.requirements.experiment_budget.maximum_elapsed_seconds
    if estimate is None or estimate.elapsed_seconds is None:
        return _result(
            capabilities,
            CompatibilityRuleId.TIME_BUDGET,
            RuleDecision.EXPERIMENTAL,
            CompatibilityReasonCode.INFORMATION_REQUIRED,
            RuleCategory.BUDGET,
            "The candidate time estimate is missing.",
            "Provide an estimated elapsed time before scheduling the candidate.",
            maximum_elapsed_seconds=maximum,
        )
    if estimate.elapsed_seconds > maximum:
        return _result(
            capabilities,
            CompatibilityRuleId.TIME_BUDGET,
            RuleDecision.REJECTED,
            CompatibilityReasonCode.TIME_BUDGET_EXCEEDED,
            RuleCategory.BUDGET,
            "The candidate estimate exceeds the customer's time budget.",
            "Reduce the candidate scope or increase the approved time budget.",
            estimated_elapsed_seconds=estimate.elapsed_seconds,
            maximum_elapsed_seconds=maximum,
        )
    return _result(
        capabilities,
        CompatibilityRuleId.TIME_BUDGET,
        RuleDecision.ALLOWED,
        CompatibilityReasonCode.CHECK_PASSED,
        RuleCategory.BUDGET,
        "The candidate estimate is within the customer's time budget.",
        estimated_elapsed_seconds=estimate.elapsed_seconds,
        maximum_elapsed_seconds=maximum,
    )


def evaluate_cost_budget(
    input_: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> RuleResult:
    estimate = input_.execution_estimate
    budget = input_.requirements.experiment_budget
    missing_cost = budget.maximum_cost_usd is not None and (
        estimate is None or estimate.cost_usd is None
    )
    if estimate is None or estimate.gpu_hours is None or missing_cost:
        return _result(
            capabilities,
            CompatibilityRuleId.COST_BUDGET,
            RuleDecision.EXPERIMENTAL,
            CompatibilityReasonCode.INFORMATION_REQUIRED,
            RuleCategory.BUDGET,
            "The cost or GPU-hour estimate required by the budget is missing.",
            "Provide explicit candidate cost and GPU-hour estimates.",
            maximum_gpu_hours=budget.maximum_gpu_hours,
            maximum_cost_usd=budget.maximum_cost_usd,
        )
    exceeds_gpu_hours = estimate.gpu_hours > budget.maximum_gpu_hours
    exceeds_cost = (
        budget.maximum_cost_usd is not None
        and estimate.cost_usd is not None
        and estimate.cost_usd > budget.maximum_cost_usd
    )
    if exceeds_gpu_hours or exceeds_cost:
        return _result(
            capabilities,
            CompatibilityRuleId.COST_BUDGET,
            RuleDecision.REJECTED,
            CompatibilityReasonCode.COST_BUDGET_EXCEEDED,
            RuleCategory.BUDGET,
            "The candidate estimate exceeds the customer's cost or GPU-hour budget.",
            "Reduce resource use or increase the approved budget.",
            estimated_gpu_hours=estimate.gpu_hours,
            maximum_gpu_hours=budget.maximum_gpu_hours,
            estimated_cost_usd=estimate.cost_usd,
            maximum_cost_usd=budget.maximum_cost_usd,
        )
    return _result(
        capabilities,
        CompatibilityRuleId.COST_BUDGET,
        RuleDecision.ALLOWED,
        CompatibilityReasonCode.CHECK_PASSED,
        RuleCategory.BUDGET,
        "The candidate estimate is within the customer's cost and GPU-hour budgets.",
        estimated_gpu_hours=estimate.gpu_hours,
        maximum_gpu_hours=budget.maximum_gpu_hours,
        estimated_cost_usd=estimate.cost_usd,
        maximum_cost_usd=budget.maximum_cost_usd,
    )


def _requested_engine_features(input_: CandidateFilterInput) -> set[str]:
    config = input_.candidate.configuration
    features = set(input_.candidate.required_capabilities)
    if config.cuda_graph:
        features.add("cuda-graph")
    if config.prefix_cache.enabled:
        features.add("prefix-cache")
    if config.prefill_decode_disaggregation:
        features.add("prefill-decode-disaggregation")
    if config.speculative_decoding.enabled:
        features.add("speculative-decoding")
    return features


def _requested_parallelism_modes(input_: CandidateFilterInput) -> set[str]:
    parallelism = input_.candidate.configuration.parallelism
    modes: set[str] = set()
    if parallelism.dp > 1:
        modes.add("data-parallel")
    if parallelism.tp > 1:
        modes.add("tensor-parallel")
    if parallelism.pp > 1:
        modes.add("pipeline-parallel")
    if parallelism.ep > 1:
        modes.add("expert-parallel")
    return modes


def evaluate_engine_features(
    input_: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> RuleResult:
    config = input_.candidate.configuration
    software = input_.hardware.software
    if (
        _normalized(config.engine) != _normalized(capabilities.engine_name)
        or _normalized(software.engine_name) != _normalized(capabilities.engine_name)
        or (
            software.engine_version is not None
            and software.engine_version != capabilities.engine_version
        )
    ):
        return _result(
            capabilities,
            CompatibilityRuleId.ENGINE_FEATURE,
            RuleDecision.REJECTED,
            CompatibilityReasonCode.ENGINE_VERSION_MISMATCH,
            RuleCategory.ENGINE_COMPATIBILITY,
            "The candidate and supplied environment do not match the pinned engine record.",
            "Use the exact engine name and version associated with this capability record.",
            expected_engine=capabilities.engine_name,
            expected_version=capabilities.engine_version,
        )
    if software.engine_version is None:
        return _result(
            capabilities,
            CompatibilityRuleId.ENGINE_FEATURE,
            RuleDecision.EXPERIMENTAL,
            CompatibilityReasonCode.ENGINE_FEATURE_UNKNOWN,
            RuleCategory.ENGINE_COMPATIBILITY,
            "The installed engine version is unknown, so pinned capabilities cannot be proven.",
            "Supply the exact installed engine version.",
        )

    unsupported: list[str] = []
    unknown: list[str] = []
    for feature in sorted(_requested_engine_features(input_)):
        state = _capability_state(capabilities.engine_features, feature)
        if state is RuleDecision.REJECTED:
            unsupported.append(feature)
        elif state is RuleDecision.EXPERIMENTAL:
            unknown.append(feature)
    for mode in sorted(_requested_parallelism_modes(input_)):
        state = _capability_state(capabilities.parallelism_modes, mode)
        if state is RuleDecision.REJECTED:
            unsupported.append(mode)
        elif state is RuleDecision.EXPERIMENTAL:
            unknown.append(mode)
    if unsupported:
        return _result(
            capabilities,
            CompatibilityRuleId.ENGINE_FEATURE,
            RuleDecision.REJECTED,
            CompatibilityReasonCode.ENGINE_FEATURE_UNSUPPORTED,
            RuleCategory.ENGINE_COMPATIBILITY,
            "One or more requested features are explicitly unsupported by the pinned engine.",
            "Disable the unsupported features or choose a verified engine version.",
            unsupported_features=", ".join(unsupported),
        )
    if unknown:
        return _result(
            capabilities,
            CompatibilityRuleId.ENGINE_FEATURE,
            RuleDecision.EXPERIMENTAL,
            CompatibilityReasonCode.ENGINE_FEATURE_UNKNOWN,
            RuleCategory.ENGINE_COMPATIBILITY,
            "One or more requested features are unknown or unverified for the pinned engine.",
            "Verify these features before execution.",
            unknown_features=", ".join(unknown),
        )
    return _result(
        capabilities,
        CompatibilityRuleId.ENGINE_FEATURE,
        RuleDecision.ALLOWED,
        CompatibilityReasonCode.CHECK_PASSED,
        RuleCategory.ENGINE_COMPATIBILITY,
        "All requested engine features are explicitly supported by the pinned record.",
        requested_feature_count=len(_requested_engine_features(input_)),
    )


def evaluate_speculative_decoding(
    input_: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> RuleResult:
    config = input_.candidate.configuration.speculative_decoding
    if not config.enabled:
        return _result(
            capabilities,
            CompatibilityRuleId.SPECULATIVE_DECODING,
            RuleDecision.ALLOWED,
            CompatibilityReasonCode.CHECK_PASSED,
            RuleCategory.ENGINE_COMPATIBILITY,
            "Speculative decoding was not requested.",
        )
    if config.draft_model_id is None or input_.draft_model is None:
        return _result(
            capabilities,
            CompatibilityRuleId.SPECULATIVE_DECODING,
            RuleDecision.REJECTED,
            CompatibilityReasonCode.SPECULATIVE_DRAFT_MODEL_REQUIRED,
            RuleCategory.ENGINE_COMPATIBILITY,
            "Speculative decoding requires supplied evidence for a compatible draft model.",
            "Select a draft model and provide its compatibility evidence.",
        )
    method = config.method
    if method is None:
        return _result(
            capabilities,
            CompatibilityRuleId.SPECULATIVE_DECODING,
            RuleDecision.EXPERIMENTAL,
            CompatibilityReasonCode.SPECULATIVE_COMPATIBILITY_UNKNOWN,
            RuleCategory.ENGINE_COMPATIBILITY,
            "The speculative decoding method was not supplied.",
            "Select a method explicitly supported by the pinned engine record.",
        )
    method_state = _capability_state(capabilities.speculative_methods, method)
    if method_state is RuleDecision.REJECTED:
        return _result(
            capabilities,
            CompatibilityRuleId.SPECULATIVE_DECODING,
            RuleDecision.REJECTED,
            CompatibilityReasonCode.ENGINE_FEATURE_UNSUPPORTED,
            RuleCategory.ENGINE_COMPATIBILITY,
            "The requested speculative decoding method is explicitly unsupported.",
            "Choose a supported method or disable speculative decoding.",
            speculative_method=method,
        )
    if method_state is RuleDecision.EXPERIMENTAL:
        return _result(
            capabilities,
            CompatibilityRuleId.SPECULATIVE_DECODING,
            RuleDecision.EXPERIMENTAL,
            CompatibilityReasonCode.SPECULATIVE_COMPATIBILITY_UNKNOWN,
            RuleCategory.ENGINE_COMPATIBILITY,
            "The requested speculative decoding method is unverified.",
            "Validate the method before execution.",
            speculative_method=method,
        )
    draft = input_.draft_model
    incompatible = (
        draft.model_id != config.draft_model_id
        or draft.tokenizer_fingerprint != input_.model.tokenizer_fingerprint
        or draft.context_length < input_.requested_context_length
        or draft.compatibility_verified is False
    )
    if incompatible:
        return _result(
            capabilities,
            CompatibilityRuleId.SPECULATIVE_DECODING,
            RuleDecision.REJECTED,
            CompatibilityReasonCode.SPECULATIVE_DRAFT_MODEL_INCOMPATIBLE,
            RuleCategory.ENGINE_COMPATIBILITY,
            "The supplied draft model is incompatible with the target model or request.",
            "Choose a verified draft model with matching tokenizer and sufficient context.",
        )
    if draft.compatibility_verified is None:
        return _result(
            capabilities,
            CompatibilityRuleId.SPECULATIVE_DECODING,
            RuleDecision.EXPERIMENTAL,
            CompatibilityReasonCode.SPECULATIVE_COMPATIBILITY_UNKNOWN,
            RuleCategory.ENGINE_COMPATIBILITY,
            "Draft-model compatibility has not been verified.",
            "Validate the draft and target model pair before execution.",
        )
    return _result(
        capabilities,
        CompatibilityRuleId.SPECULATIVE_DECODING,
        RuleDecision.ALLOWED,
        CompatibilityReasonCode.CHECK_PASSED,
        RuleCategory.ENGINE_COMPATIBILITY,
        "The supplied draft-model evidence satisfies speculative decoding checks.",
        speculative_method=method,
    )


def evaluate_expert_parallelism(
    input_: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> RuleResult:
    ep = input_.candidate.configuration.parallelism.ep
    if ep > 1 and input_.model.dense_or_moe is not ModelTopology.MOE:
        return _result(
            capabilities,
            CompatibilityRuleId.EXPERT_PARALLELISM,
            RuleDecision.REJECTED,
            CompatibilityReasonCode.EXPERT_PARALLELISM_REQUIRES_MOE,
            RuleCategory.ENGINE_COMPATIBILITY,
            "Expert parallelism can only be used with an explicitly identified MoE model.",
            "Disable expert parallelism or select a verified MoE model.",
            expert_parallel_size=ep,
        )
    return _result(
        capabilities,
        CompatibilityRuleId.EXPERT_PARALLELISM,
        RuleDecision.ALLOWED,
        CompatibilityReasonCode.CHECK_PASSED,
        RuleCategory.ENGINE_COMPATIBILITY,
        "The model topology is compatible with the requested expert-parallel setting.",
        expert_parallel_size=ep,
    )


def evaluate_orionix_certification(
    input_: CandidateFilterInput, capabilities: EngineCapabilityRecord
) -> RuleResult:
    accelerators = _candidate_accelerators(input_)
    precision = input_.candidate.configuration.precision or input_.model.dtype
    quantization = input_.model.quantization
    features = {_normalized(item) for item in _requested_engine_features(input_)}
    features.update(_normalized(item) for item in _requested_parallelism_modes(input_))
    for profile in capabilities.certification_profiles:
        if (
            profile.engine_version == capabilities.engine_version
            and _normalized(profile.model_architecture) == _normalized(input_.model.architecture)
            and _normalized(profile.precision) == _normalized(precision)
            and profile.quantization == quantization
            and features <= {_normalized(item) for item in profile.features}
            and accelerators
            and all(
                _normalized(accelerator.vendor) == _normalized(profile.accelerator_vendor)
                and _normalized(accelerator.architecture_family)
                == _normalized(profile.accelerator_architecture)
                for accelerator in accelerators
            )
        ):
            return _result(
                capabilities,
                CompatibilityRuleId.ORIONIX_CERTIFICATION,
                RuleDecision.ALLOWED,
                CompatibilityReasonCode.CHECK_PASSED,
                RuleCategory.ORIONIX_CERTIFICATION,
                "This exact synthetic profile matches retained Orionix certification evidence.",
                certification_profile_id=profile.profile_id,
            )
    return _result(
        capabilities,
        CompatibilityRuleId.ORIONIX_CERTIFICATION,
        RuleDecision.EXPERIMENTAL,
        CompatibilityReasonCode.ENGINE_COMPATIBLE_NOT_CERTIFIED,
        RuleCategory.ORIONIX_CERTIFICATION,
        "Engine compatibility does not mean this exact configuration is Orionix certified.",
        "Run the required validation process before making a certification claim.",
    )


RULES: tuple[Rule, ...] = (
    evaluate_gpu_memory,
    evaluate_gpu_architecture,
    evaluate_precision,
    evaluate_quantization,
    evaluate_context_length,
    evaluate_tensor_parallel_size,
    evaluate_parallelism_topology,
    evaluate_time_budget,
    evaluate_cost_budget,
    evaluate_engine_features,
    evaluate_speculative_decoding,
    evaluate_expert_parallelism,
    evaluate_orionix_certification,
)


def _aggregate(decisions: Iterable[RuleDecision]) -> RuleDecision:
    values = tuple(decisions)
    if RuleDecision.REJECTED in values:
        return RuleDecision.REJECTED
    if RuleDecision.EXPERIMENTAL in values:
        return RuleDecision.EXPERIMENTAL
    return RuleDecision.ALLOWED


class CandidateCompatibilityEvaluator:
    """Evaluates every rule in stable order and never invokes an execution backend."""

    def evaluate(
        self, input_: CandidateFilterInput, capabilities: EngineCapabilityRecord
    ) -> CandidateFilterResult:
        results = tuple(rule(input_, capabilities) for rule in RULES)
        certification = next(
            result for result in results if result.category is RuleCategory.ORIONIX_CERTIFICATION
        )
        engine_results = (
            result
            for result in results
            if result.category in {RuleCategory.ENGINE_COMPATIBILITY, RuleCategory.TOPOLOGY}
        )
        return CandidateFilterResult(
            schema_version=CandidateFilterResult.SCHEMA_VERSION,
            configuration_id=input_.candidate.configuration_id,
            decision=_aggregate(result.decision for result in results),
            engine_compatibility=_aggregate(result.decision for result in engine_results),
            orionix_certification=certification.decision,
            rule_results=results,
        )

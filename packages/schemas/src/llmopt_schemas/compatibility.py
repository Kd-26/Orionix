"""Versioned compatibility capabilities, decisions, and fingerprint metadata."""

from datetime import date
from enum import StrEnum
from typing import ClassVar

from llmopt_common import ConfigurationId
from pydantic import Field, JsonValue, model_validator

from llmopt_schemas.base import ContractModel
from llmopt_schemas.serving import ParallelismConfig


class RuleDecision(StrEnum):
    """The only decisions a Day 4 compatibility rule may return."""

    ALLOWED = "allowed"
    REJECTED = "rejected"
    EXPERIMENTAL = "experimental"


class RuleCategory(StrEnum):
    ENGINE_COMPATIBILITY = "engine_compatibility"
    ORIONIX_CERTIFICATION = "orionix_certification"
    RESOURCE = "resource"
    TOPOLOGY = "topology"
    BUDGET = "budget"


class CompatibilityRuleId(StrEnum):
    GPU_MEMORY = "gpu_memory"
    GPU_ARCHITECTURE = "gpu_architecture"
    PRECISION = "precision"
    QUANTIZATION = "quantization"
    CONTEXT_LENGTH = "context_length"
    TENSOR_PARALLEL_SIZE = "tensor_parallel_size"
    PARALLELISM_TOPOLOGY = "parallelism_topology"
    TIME_BUDGET = "time_budget"
    COST_BUDGET = "cost_budget"
    ENGINE_FEATURE = "engine_feature"
    SPECULATIVE_DECODING = "speculative_decoding"
    EXPERT_PARALLELISM = "expert_parallelism"
    ORIONIX_CERTIFICATION = "orionix_certification"


class CompatibilityReasonCode(StrEnum):
    """Stable public identifiers; messages may improve without changing these values."""

    CHECK_PASSED = "CHECK_PASSED"
    INFORMATION_REQUIRED = "INFORMATION_REQUIRED"
    INSUFFICIENT_GPU_MEMORY = "INSUFFICIENT_GPU_MEMORY"
    UNSUPPORTED_GPU_ARCHITECTURE = "UNSUPPORTED_GPU_ARCHITECTURE"
    UNKNOWN_GPU_ARCHITECTURE = "UNKNOWN_GPU_ARCHITECTURE"
    UNSUPPORTED_PRECISION = "UNSUPPORTED_PRECISION"
    UNKNOWN_PRECISION_SUPPORT = "UNKNOWN_PRECISION_SUPPORT"
    UNSUPPORTED_QUANTIZATION = "UNSUPPORTED_QUANTIZATION"
    UNKNOWN_QUANTIZATION_SUPPORT = "UNKNOWN_QUANTIZATION_SUPPORT"
    CONTEXT_LENGTH_EXCEEDS_ENGINE_LIMIT = "CONTEXT_LENGTH_EXCEEDS_ENGINE_LIMIT"
    ENGINE_CONTEXT_LIMIT_UNKNOWN = "ENGINE_CONTEXT_LIMIT_UNKNOWN"
    INVALID_TENSOR_PARALLEL_SIZE = "INVALID_TENSOR_PARALLEL_SIZE"
    PARALLELISM_TOPOLOGY_MISMATCH = "PARALLELISM_TOPOLOGY_MISMATCH"
    TOPOLOGY_INFORMATION_REQUIRED = "TOPOLOGY_INFORMATION_REQUIRED"
    TIME_BUDGET_EXCEEDED = "TIME_BUDGET_EXCEEDED"
    COST_BUDGET_EXCEEDED = "COST_BUDGET_EXCEEDED"
    ENGINE_FEATURE_UNSUPPORTED = "ENGINE_FEATURE_UNSUPPORTED"
    ENGINE_FEATURE_UNKNOWN = "ENGINE_FEATURE_UNKNOWN"
    ENGINE_VERSION_MISMATCH = "ENGINE_VERSION_MISMATCH"
    SPECULATIVE_DRAFT_MODEL_REQUIRED = "SPECULATIVE_DRAFT_MODEL_REQUIRED"
    SPECULATIVE_DRAFT_MODEL_INCOMPATIBLE = "SPECULATIVE_DRAFT_MODEL_INCOMPATIBLE"
    SPECULATIVE_COMPATIBILITY_UNKNOWN = "SPECULATIVE_COMPATIBILITY_UNKNOWN"
    EXPERT_PARALLELISM_REQUIRES_MOE = "EXPERT_PARALLELISM_REQUIRES_MOE"
    ENGINE_COMPATIBLE_NOT_CERTIFIED = "ENGINE_COMPATIBLE_NOT_CERTIFIED"


class CapabilityValues(ContractModel):
    """Explicit three-way knowledge for string-valued capabilities."""

    supported: tuple[str, ...] = ()
    unsupported: tuple[str, ...] = ()
    unverified: tuple[str, ...] = ()

    @model_validator(mode="after")
    def values_do_not_overlap(self) -> "CapabilityValues":
        groups = tuple(
            {item.strip().casefold().replace("_", "-") for item in values}
            for values in (self.supported, self.unsupported, self.unverified)
        )
        if groups[0] & groups[1] or groups[0] & groups[2] or groups[1] & groups[2]:
            raise ValueError("capability values cannot appear in more than one support state")
        return self


class AcceleratorEngineCapability(ContractModel):
    vendor: str = Field(min_length=1)
    architecture_family: str = Field(min_length=1)
    precisions: CapabilityValues
    quantizations: CapabilityValues


class CapabilityProvenance(ContractModel):
    source: str = Field(min_length=1)
    verified_on: date | None = None
    synthetic: bool
    notes: str | None = None


class CertificationProfile(ContractModel):
    """One exact, retained Orionix certification claim."""

    profile_id: str = Field(min_length=1)
    engine_version: str = Field(min_length=1)
    accelerator_vendor: str = Field(min_length=1)
    accelerator_architecture: str = Field(min_length=1)
    model_architecture: str = Field(min_length=1)
    precision: str = Field(min_length=1)
    quantization: str | None = None
    features: tuple[str, ...] = ()
    evidence_reference: str = Field(min_length=1)


class EngineCapabilityRecord(ContractModel):
    """Declarative facts for one exact engine version; it contains no adapter code."""

    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    record_version: str = Field(min_length=1)
    engine_name: str = Field(min_length=1)
    engine_version: str = Field(min_length=1)
    accelerator_capabilities: tuple[AcceleratorEngineCapability, ...]
    explicitly_unsupported_architectures: tuple[str, ...] = ()
    maximum_context_length: int | None = Field(default=None, ge=1)
    maximum_tensor_parallel_size: int | None = Field(default=None, ge=1)
    parallelism_modes: CapabilityValues
    engine_features: CapabilityValues
    speculative_methods: CapabilityValues
    certification_profiles: tuple[CertificationProfile, ...] = ()
    provenance: CapabilityProvenance

    @model_validator(mode="after")
    def architecture_rows_are_unique(self) -> "EngineCapabilityRecord":
        keys = [
            (
                item.vendor.casefold(),
                item.architecture_family.casefold().replace("_", "-"),
            )
            for item in self.accelerator_capabilities
        ]
        if len(keys) != len(set(keys)):
            raise ValueError("engine capability architecture rows must be unique")
        supported_architectures = {key[1] for key in keys}
        unsupported_architectures = {
            item.casefold().replace("_", "-") for item in self.explicitly_unsupported_architectures
        }
        if supported_architectures & unsupported_architectures:
            raise ValueError("an architecture cannot be both supported and unsupported")
        profile_ids = [profile.profile_id for profile in self.certification_profiles]
        if len(profile_ids) != len(set(profile_ids)):
            raise ValueError("certification profile identifiers must be unique")
        return self


class RuleResult(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    rule_id: CompatibilityRuleId
    decision: RuleDecision
    reason_code: CompatibilityReasonCode
    category: RuleCategory
    message: str = Field(min_length=1)
    remediation: str | None = None
    evidence: dict[str, str | int | float | bool | None] = Field(default_factory=dict)
    capability_record_version: str
    rule_version: str


class CandidateFilterResult(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    configuration_id: ConfigurationId
    decision: RuleDecision
    engine_compatibility: RuleDecision
    orionix_certification: RuleDecision
    rule_results: tuple[RuleResult, ...] = Field(min_length=1)


class CompatibilityLayer(StrEnum):
    MODEL = "model"
    HARDWARE_KERNEL = "hardware_kernel"
    ENGINE_RUNTIME = "engine_runtime"
    CUDA_GRAPH = "cuda_graph"
    MEMORY = "memory"
    SERVING_POLICY = "serving_policy"
    WORKLOAD_POLICY = "workload_policy"
    PROVIDER_EXECUTION = "provider_execution"


class CompatibilityFingerprint(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    model_hash: str
    model_revision: str | None = None
    execution_backend: str
    provider_name: str | None = None
    provider_region: str | None = None
    provider_instance_type: str | None = None
    provider_resource_identifier_hash: str | None = None
    physical_gpu_model: str | None = None
    gpu_architecture: str | None = None
    gpu_count: int | None = Field(default=None, ge=0)
    vram_bytes_per_gpu: int | None = Field(default=None, ge=0)
    gpu_topology: str | None = None
    cpu_count: int | None = Field(default=None, ge=1)
    ram_bytes: int | None = Field(default=None, ge=0)
    storage_class: str | None = None
    filesystem_type: str | None = None
    virtualization_type: str | None = None
    container_type: str | None = None
    cuda_version: str | None = None
    driver_version: str | None = None
    pytorch_version: str | None = None
    engine: str
    engine_version: str | None = None
    engine_image_digest: str | None = None
    kernel_library_versions: dict[str, str] = Field(default_factory=dict)
    precision: str | None = None
    parallelism: ParallelismConfig = Field(default_factory=ParallelismConfig)
    kv_cache_layout_version: str | None = None
    capsule_schema_version: str
    layer_fingerprints: dict[CompatibilityLayer, str] = Field(default_factory=dict)
    provider_extensions: dict[str, JsonValue] = Field(default_factory=dict)

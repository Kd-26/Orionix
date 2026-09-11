"""Lifecycle values; orchestration behavior intentionally lives elsewhere."""

from enum import StrEnum


class OptimizationJobState(StrEnum):
    """Future control-plane optimization job states."""

    PENDING = "PENDING"
    INSPECTING = "INSPECTING"
    ANALYZING = "ANALYZING"
    BENCHMARKING = "BENCHMARKING"
    OPTIMIZING = "OPTIMIZING"
    VALIDATING = "VALIDATING"
    PACKAGING = "PACKAGING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class CapsuleState(StrEnum):
    """Future Execution Capsule lifecycle states."""

    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    ACTIVE = "ACTIVE"
    STALE = "STALE"
    INCOMPATIBLE = "INCOMPATIBLE"
    RETIRED = "RETIRED"

"""Lifecycle values; orchestration behavior intentionally lives elsewhere."""

from enum import StrEnum


class OptimizationJobState(StrEnum):
    """Future control-plane optimization job states."""

    PENDING = "PENDING"
    CLAIMED = "CLAIMED"
    INSPECTING = "INSPECTING"
    ANALYZING = "ANALYZING"
    BENCHMARKING = "BENCHMARKING"
    OPTIMIZING = "OPTIMIZING"
    VALIDATING = "VALIDATING"
    PACKAGING = "PACKAGING"
    CANCELLING = "CANCELLING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    CANCELLED = "CANCELLED"


class CapsuleState(StrEnum):
    """Future Execution Capsule lifecycle states."""

    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    ACTIVE = "ACTIVE"
    STALE = "STALE"
    INCOMPATIBLE = "INCOMPATIBLE"
    RETIRED = "RETIRED"


class ComputeState(StrEnum):
    """Provider-neutral compute-target states."""

    REQUESTED = "REQUESTED"
    PROVISIONING = "PROVISIONING"
    READY = "READY"
    BUSY = "BUSY"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"
    TERMINATED = "TERMINATED"

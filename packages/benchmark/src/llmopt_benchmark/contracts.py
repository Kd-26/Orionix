"""Benchmark orchestration data, separate from observed result schemas."""

from enum import StrEnum
from typing import ClassVar

from llmopt_common import AttemptId, BenchmarkRunId
from llmopt_schemas import (
    CompatibilityFingerprint,
    HardwareSpec,
    ModelSpec,
    ServingConfig,
    WorkloadSpec,
)
from llmopt_schemas.base import ContractModel
from pydantic import Field


class BenchmarkRunState(StrEnum):
    PLANNED = "planned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BenchmarkEnvironment(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    fingerprint: CompatibilityFingerprint
    hardware: HardwareSpec
    labels: dict[str, str] = Field(default_factory=dict)


class BenchmarkPlan(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    plan_id: str
    model: ModelSpec
    workload: WorkloadSpec
    configurations: tuple[ServingConfig, ...]
    warmup_seconds: float = Field(default=0, ge=0)
    measurement_seconds: float = Field(gt=0)
    request_timeout_seconds: float = Field(gt=0)


class BenchmarkRun(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    run_id: BenchmarkRunId
    attempt_id: AttemptId
    plan: BenchmarkPlan
    environment: BenchmarkEnvironment
    state: BenchmarkRunState = BenchmarkRunState.PLANNED

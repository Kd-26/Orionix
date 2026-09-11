"""Benchmark orchestration data, separate from observed result schemas."""

from enum import StrEnum

from llmopt_domain import BenchmarkRunId
from llmopt_schemas import HardwareSpec, ModelSpec, ServingConfig, WorkloadSpec
from llmopt_schemas.base import ContractModel
from pydantic import Field


class BenchmarkRunState(StrEnum):
    PLANNED = "planned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BenchmarkEnvironment(ContractModel):
    fingerprint: str
    hardware: HardwareSpec
    labels: dict[str, str] = Field(default_factory=dict)


class BenchmarkPlan(ContractModel):
    model: ModelSpec
    workload: WorkloadSpec
    configurations: tuple[ServingConfig, ...]
    warmup_seconds: float = Field(default=0, ge=0)
    measurement_seconds: float = Field(gt=0)


class BenchmarkRun(ContractModel):
    run_id: BenchmarkRunId
    plan: BenchmarkPlan
    environment: BenchmarkEnvironment
    state: BenchmarkRunState = BenchmarkRunState.PLANNED

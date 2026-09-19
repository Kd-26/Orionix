"""Benchmark result data contract."""

from datetime import datetime
from typing import ClassVar

from llmopt_common import BenchmarkRunId, ConfigurationId
from pydantic import Field, model_validator

from llmopt_schemas.base import ContractModel


class MetricDistribution(ContractModel):
    p50: float | None = Field(default=None, ge=0)
    p95: float | None = Field(default=None, ge=0)
    p99: float | None = Field(default=None, ge=0)


class RatioDistribution(ContractModel):
    p50: float | None = Field(default=None, ge=0, le=1)
    p95: float | None = Field(default=None, ge=0, le=1)
    p99: float | None = Field(default=None, ge=0, le=1)


class BenchmarkErrorRecord(ContractModel):
    category: str
    count: int = Field(ge=1)
    sanitized_message: str | None = None


class ArtifactReference(ContractModel):
    artifact_id: str = Field(min_length=1)
    kind: str = Field(min_length=1)
    reference: str = Field(min_length=1)
    digest: str = Field(pattern=r"^sha256:[0-9a-f]{64}$")
    media_type: str | None = None
    redacted: bool = True


class BenchmarkResult(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "2.0"

    schema_version: str = SCHEMA_VERSION
    run_id: BenchmarkRunId | None = None
    configuration_id: ConfigurationId
    ttft_ms: MetricDistribution
    tpot_ms: MetricDistribution
    end_to_end_latency_ms: MetricDistribution | None = None
    generated_tokens_per_second: float | None = Field(default=None, ge=0)
    total_tokens_per_second: float | None = Field(default=None, ge=0)
    requests_per_second: float = Field(ge=0)
    goodput_requests_per_second: float | None = Field(default=None, ge=0)
    gpu_utilization_ratio: RatioDistribution | None = None
    vram_utilization_ratio: RatioDistribution | None = None
    cost_per_token_usd: float | None = Field(default=None, ge=0)
    total_cost_usd: float | None = Field(default=None, ge=0)
    generated_token_count: int = Field(default=0, ge=0)
    total_token_count: int = Field(default=0, ge=0)
    completed_request_count: int = Field(default=0, ge=0)
    failed_request_count: int = Field(default=0, ge=0)
    cancelled_request_count: int = Field(default=0, ge=0)
    errors: tuple[BenchmarkErrorRecord, ...] = ()
    artifacts: tuple[ArtifactReference, ...] = ()
    oom_events: int = Field(default=0, ge=0)
    provisioning_duration_seconds: float | None = Field(default=None, ge=0)
    cold_start_duration_seconds: float | None = Field(default=None, ge=0)
    model_load_duration_seconds: float | None = Field(default=None, ge=0)
    duration_seconds: float = Field(gt=0)
    environment_fingerprint: str
    workload_fingerprint: str
    partial: bool = False
    started_at: datetime | None = None
    finished_at: datetime | None = None

    @model_validator(mode="after")
    def validate_timestamps(self) -> "BenchmarkResult":
        if (
            self.started_at is not None
            and self.finished_at is not None
            and self.finished_at < self.started_at
        ):
            raise ValueError("benchmark finish time cannot precede start time")
        return self

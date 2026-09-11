"""Benchmark result data contract."""

from datetime import datetime
from typing import ClassVar

from llmopt_domain import ConfigurationId
from pydantic import Field

from llmopt_schemas.base import ContractModel


class MetricDistribution(ContractModel):
    p50: float | None = Field(default=None, ge=0)
    p95: float | None = Field(default=None, ge=0)
    p99: float | None = Field(default=None, ge=0)


class BenchmarkErrorRecord(ContractModel):
    category: str
    count: int = Field(ge=1)
    message: str | None = None


class BenchmarkResult(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    configuration_id: ConfigurationId
    ttft_ms: MetricDistribution
    tpot_ms: MetricDistribution
    tokens_per_second: float = Field(ge=0)
    requests_per_second: float = Field(ge=0)
    goodput: float = Field(ge=0)
    gpu_utilization: MetricDistribution | None = None
    vram_utilization: MetricDistribution | None = None
    cost: float | None = Field(default=None, ge=0)
    errors: tuple[BenchmarkErrorRecord, ...] = ()
    oom_events: int = Field(default=0, ge=0)
    duration_seconds: float = Field(gt=0)
    environment_fingerprint: str
    started_at: datetime | None = None

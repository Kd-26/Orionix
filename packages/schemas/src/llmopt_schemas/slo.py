"""Service-level objective contract."""

from typing import ClassVar

from pydantic import Field

from llmopt_schemas.base import ContractModel


class SLOSpec(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    p50_ttft_ms: float | None = Field(default=None, gt=0)
    p95_ttft_ms: float | None = Field(default=None, gt=0)
    p99_ttft_ms: float | None = Field(default=None, gt=0)
    p50_tpot_ms: float | None = Field(default=None, gt=0)
    p95_tpot_ms: float | None = Field(default=None, gt=0)
    minimum_throughput_tokens_per_second: float | None = Field(default=None, ge=0)
    maximum_cost_per_token_usd: float | None = Field(default=None, ge=0)
    maximum_quality_loss: float | None = Field(default=None, ge=0)
    maximum_error_rate: float | None = Field(default=None, ge=0, le=1)

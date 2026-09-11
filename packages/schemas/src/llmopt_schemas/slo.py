"""Service-level objective contract."""

from pydantic import Field

from llmopt_schemas.base import ContractModel


class SLOSpec(ContractModel):
    p50_ttft_ms: float | None = Field(default=None, gt=0)
    p95_ttft_ms: float | None = Field(default=None, gt=0)
    p99_ttft_ms: float | None = Field(default=None, gt=0)
    p50_tpot_ms: float | None = Field(default=None, gt=0)
    p95_tpot_ms: float | None = Field(default=None, gt=0)
    minimum_throughput_tokens_per_second: float | None = Field(default=None, ge=0)
    maximum_cost_per_token: float | None = Field(default=None, ge=0)
    maximum_quality_loss: float | None = Field(default=None, ge=0)
    maximum_error_rate: float | None = Field(default=None, ge=0, le=1)

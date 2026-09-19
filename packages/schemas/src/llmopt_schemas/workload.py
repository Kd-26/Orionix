"""Workload distribution contracts; no analysis behavior."""

from typing import ClassVar

from pydantic import Field, model_validator

from llmopt_schemas.base import ContractModel


class TokenDistribution(ContractModel):
    p50: int = Field(ge=0)
    p95: int = Field(ge=0)
    max: int = Field(ge=0)

    @model_validator(mode="after")
    def ordered_percentiles(self) -> "TokenDistribution":
        if not self.p50 <= self.p95 <= self.max:
            raise ValueError("token distribution must satisfy p50 <= p95 <= max")
        return self


class ConcurrencyDistribution(ContractModel):
    median: int = Field(ge=0)
    peak: int = Field(ge=0)

    @model_validator(mode="after")
    def ordered_values(self) -> "ConcurrencyDistribution":
        if self.median > self.peak:
            raise ValueError("concurrency must satisfy median <= peak")
        return self


class RequestRateDistribution(ContractModel):
    average: float = Field(ge=0)
    peak: float = Field(ge=0)

    @model_validator(mode="after")
    def ordered_values(self) -> "RequestRateDistribution":
        if self.average > self.peak:
            raise ValueError("request rate must satisfy average <= peak")
        return self


class WorkloadSpec(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    input_tokens: TokenDistribution
    output_tokens: TokenDistribution
    concurrency: ConcurrencyDistribution
    request_rate: RequestRateDistribution
    streaming: bool
    prefix_reuse_probability: float | None = Field(default=None, ge=0, le=1)
    average_reusable_prefix_tokens: float | None = Field(default=None, ge=0)
    workload_fingerprint: str = Field(pattern=r"^sha256:[0-9a-f]{64}$")

"""Engine-neutral serving configuration contract."""

from pydantic import Field

from llmopt_schemas.base import ContractModel


class ParallelismConfig(ContractModel):
    dp: int = Field(default=1, ge=1)
    tp: int = Field(default=1, ge=1)
    pp: int = Field(default=1, ge=1)
    ep: int = Field(default=1, ge=1)


class ServingConfig(ContractModel):
    engine: str
    parallelism: ParallelismConfig = Field(default_factory=ParallelismConfig)
    precision: str | None = None
    cuda_graph: bool | None = None
    batching: dict[str, str | int | float | bool] = Field(default_factory=dict)
    scheduler: dict[str, str | int | float | bool] = Field(default_factory=dict)
    kv_cache: dict[str, str | int | float | bool] = Field(default_factory=dict)
    prefix_cache: dict[str, str | int | float | bool] = Field(default_factory=dict)
    speculative_decoding: dict[str, str | int | float | bool] = Field(default_factory=dict)
    prefill_decode_disaggregation: dict[str, str | int | float | bool] = Field(default_factory=dict)
    memory: dict[str, str | int | float | bool] = Field(default_factory=dict)
    autoscaling: dict[str, str | int | float | bool] = Field(default_factory=dict)

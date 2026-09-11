"""Engine-neutral serving configuration contract."""

from typing import ClassVar

from pydantic import Field

from llmopt_schemas.base import ContractModel


class ParallelismConfig(ContractModel):
    dp: int = Field(default=1, ge=1)
    tp: int = Field(default=1, ge=1)
    pp: int = Field(default=1, ge=1)
    ep: int = Field(default=1, ge=1)


class BatchingConfig(ContractModel):
    max_sequences: int | None = Field(default=None, ge=1)
    max_batch_tokens: int | None = Field(default=None, ge=1)


class SchedulerConfig(ContractModel):
    policy: str | None = None


class KvCacheConfig(ContractModel):
    block_size_tokens: int | None = Field(default=None, ge=1)
    dtype: str | None = None


class PrefixCacheConfig(ContractModel):
    enabled: bool = False


class SpeculativeDecodingConfig(ContractModel):
    enabled: bool = False
    draft_model_id: str | None = None


class MemoryConfig(ContractModel):
    gpu_memory_utilization_ratio: float | None = Field(default=None, gt=0, le=1)
    swap_space_bytes: int | None = Field(default=None, ge=0)


class AutoscalingConfig(ContractModel):
    enabled: bool = False
    minimum_replicas: int = Field(default=1, ge=0)
    maximum_replicas: int = Field(default=1, ge=1)


class ServingConfig(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    engine: str
    parallelism: ParallelismConfig = Field(default_factory=ParallelismConfig)
    precision: str | None = None
    cuda_graph: bool | None = None
    batching: BatchingConfig = Field(default_factory=BatchingConfig)
    scheduler: SchedulerConfig = Field(default_factory=SchedulerConfig)
    kv_cache: KvCacheConfig = Field(default_factory=KvCacheConfig)
    prefix_cache: PrefixCacheConfig = Field(default_factory=PrefixCacheConfig)
    speculative_decoding: SpeculativeDecodingConfig = Field(
        default_factory=SpeculativeDecodingConfig
    )
    prefill_decode_disaggregation: bool = False
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    autoscaling: AutoscalingConfig = Field(default_factory=AutoscalingConfig)

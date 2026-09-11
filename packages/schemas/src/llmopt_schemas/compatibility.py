"""Layered compatibility fingerprint metadata; no invalidation behavior."""

from enum import StrEnum

from pydantic import Field

from llmopt_schemas.base import ContractModel
from llmopt_schemas.serving import ParallelismConfig


class CompatibilityLayer(StrEnum):
    MODEL = "model"
    KERNEL = "kernel"
    CUDA_GRAPH = "cuda_graph"
    MEMORY = "memory"
    SERVING_POLICY = "serving_policy"
    WORKLOAD_POLICY = "workload_policy"


class CompatibilityFingerprint(ContractModel):
    model_hash: str
    model_revision: str | None = None
    gpu_architecture: str | None = None
    gpu_count: int | None = Field(default=None, ge=0)
    cuda_version: str | None = None
    driver_version: str | None = None
    pytorch_version: str | None = None
    engine: str
    engine_version: str | None = None
    kernel_library_versions: dict[str, str] = Field(default_factory=dict)
    precision: str | None = None
    parallelism: ParallelismConfig = Field(default_factory=ParallelismConfig)
    kv_cache_layout_version: str | None = None
    capsule_schema_version: str
    layer_fingerprints: dict[CompatibilityLayer, str] = Field(default_factory=dict)

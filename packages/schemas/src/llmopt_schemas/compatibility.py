"""Layered compatibility fingerprint metadata; no invalidation behavior."""

from enum import StrEnum
from typing import ClassVar

from pydantic import Field, JsonValue

from llmopt_schemas.base import ContractModel
from llmopt_schemas.serving import ParallelismConfig


class CompatibilityLayer(StrEnum):
    MODEL = "model"
    HARDWARE_KERNEL = "hardware_kernel"
    ENGINE_RUNTIME = "engine_runtime"
    CUDA_GRAPH = "cuda_graph"
    MEMORY = "memory"
    SERVING_POLICY = "serving_policy"
    WORKLOAD_POLICY = "workload_policy"
    PROVIDER_EXECUTION = "provider_execution"


class CompatibilityFingerprint(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    model_hash: str
    model_revision: str | None = None
    execution_backend: str
    provider_name: str | None = None
    provider_region: str | None = None
    provider_instance_type: str | None = None
    provider_resource_identifier_hash: str | None = None
    physical_gpu_model: str | None = None
    gpu_architecture: str | None = None
    gpu_count: int | None = Field(default=None, ge=0)
    vram_bytes_per_gpu: int | None = Field(default=None, ge=0)
    gpu_topology: str | None = None
    cpu_count: int | None = Field(default=None, ge=1)
    ram_bytes: int | None = Field(default=None, ge=0)
    storage_class: str | None = None
    filesystem_type: str | None = None
    virtualization_type: str | None = None
    container_type: str | None = None
    cuda_version: str | None = None
    driver_version: str | None = None
    pytorch_version: str | None = None
    engine: str
    engine_version: str | None = None
    engine_image_digest: str | None = None
    kernel_library_versions: dict[str, str] = Field(default_factory=dict)
    precision: str | None = None
    parallelism: ParallelismConfig = Field(default_factory=ParallelismConfig)
    kv_cache_layout_version: str | None = None
    capsule_schema_version: str
    layer_fingerprints: dict[CompatibilityLayer, str] = Field(default_factory=dict)
    provider_extensions: dict[str, JsonValue] = Field(default_factory=dict)

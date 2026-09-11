"""Hardware/environment metadata contract."""

from typing import ClassVar

from pydantic import Field

from llmopt_schemas.base import ContractModel


class HardwareSpec(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    cpu_model: str | None = None
    cpu_count: int | None = Field(default=None, ge=1)
    ram_bytes: int | None = Field(default=None, ge=0)
    gpu_model: str | None = None
    gpu_architecture: str | None = None
    gpu_count: int = Field(default=0, ge=0)
    vram_bytes_per_gpu: int | None = Field(default=None, ge=0)
    nvlink_available: bool | None = None
    gpu_topology: str | None = None
    storage_bytes: int | None = Field(default=None, ge=0)
    storage_class: str | None = None
    filesystem_type: str | None = None
    cuda_version: str | None = None
    driver_version: str | None = None
    nccl_version: str | None = None

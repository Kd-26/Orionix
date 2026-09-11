"""Hardware/environment metadata contract."""

from pydantic import Field

from llmopt_schemas.base import ContractModel


class HardwareSpec(ContractModel):
    gpu_model: str | None = None
    gpu_architecture: str | None = None
    gpu_count: int = Field(default=0, ge=0)
    vram_gib_per_gpu: float | None = Field(default=None, ge=0)
    nvlink_available: bool | None = None
    pcie_topology: str | None = None
    cpu: str | None = None
    ram_gib: float | None = Field(default=None, ge=0)
    nvme_gib: float | None = Field(default=None, ge=0)
    cuda_version: str | None = None
    driver_version: str | None = None
    nccl_version: str | None = None

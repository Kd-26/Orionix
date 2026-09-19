"""Model metadata contract."""

from enum import StrEnum
from typing import ClassVar

from pydantic import Field, model_validator

from llmopt_schemas.base import ContractModel


class ModelTopology(StrEnum):
    DENSE = "dense"
    MOE = "moe"


class ModelSpec(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    model_id: str = Field(min_length=1)
    revision: str = Field(min_length=1)
    architecture: str = Field(min_length=1)
    parameter_count: int = Field(gt=0)
    model_type: str | None = None
    dense_or_moe: ModelTopology
    num_layers: int | None = Field(default=None, gt=0)
    num_experts: int | None = Field(default=None, ge=0)
    active_experts: int | None = Field(default=None, ge=0)
    context_length: int = Field(ge=1)
    dtype: str = Field(min_length=1)
    quantization: str | None = None
    tokenizer_fingerprint: str = Field(pattern=r"^sha256:[0-9a-f]{64}$")
    model_fingerprint: str = Field(pattern=r"^sha256:[0-9a-f]{64}$")

    @model_validator(mode="after")
    def validate_model_topology(self) -> "ModelSpec":
        if self.dense_or_moe is ModelTopology.DENSE and (
            self.num_experts is not None or self.active_experts is not None
        ):
            raise ValueError("dense models cannot declare expert counts")
        if self.dense_or_moe is ModelTopology.MOE:
            if self.num_experts is None or self.active_experts is None:
                raise ValueError("MoE models require total and active expert counts")
            if self.active_experts > self.num_experts:
                raise ValueError("active expert count cannot exceed total expert count")
        return self

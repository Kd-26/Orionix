"""Model metadata contract."""

from enum import StrEnum
from typing import ClassVar

from pydantic import Field

from llmopt_schemas.base import ContractModel


class ModelTopology(StrEnum):
    DENSE = "dense"
    MOE = "moe"


class ModelSpec(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    model_id: str
    revision: str | None = None
    architecture: str | None = None
    parameter_count: int | None = Field(default=None, ge=0)
    model_type: str | None = None
    dense_or_moe: ModelTopology | None = None
    num_layers: int | None = Field(default=None, ge=0)
    num_experts: int | None = Field(default=None, ge=0)
    active_experts: int | None = Field(default=None, ge=0)
    context_length: int | None = Field(default=None, ge=1)
    dtype: str | None = None
    quantization: str | None = None

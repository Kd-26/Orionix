"""Base behavior shared by versioned contracts."""

from pydantic import BaseModel, ConfigDict


class ContractModel(BaseModel):
    """Strict, immutable base for cross-boundary data."""

    model_config = ConfigDict(extra="forbid", frozen=True)

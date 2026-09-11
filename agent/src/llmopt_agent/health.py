"""Agent health/version metadata only; no server is implemented."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class HealthStatus(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"


class AgentHealth(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: HealthStatus = HealthStatus.HEALTHY
    version: str = "0.1.0.dev0"

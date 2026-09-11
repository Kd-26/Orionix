"""Non-secret agent configuration contract."""

from pydantic import BaseModel, ConfigDict, Field


class AgentConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    agent_id: str
    control_plane_url: str | None = None
    allow_external_telemetry: bool = False
    health_port: int = Field(default=8081, ge=1, le=65535)

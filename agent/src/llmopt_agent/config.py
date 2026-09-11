"""Non-secret agent configuration contract."""

from llmopt_common import AgentId
from pydantic import BaseModel, ConfigDict, Field, SecretStr


class AgentConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    agent_id: AgentId
    control_plane_url: str | None = None
    credential: SecretStr | None = None
    allow_external_telemetry: bool = False
    health_port: int = Field(default=8081, ge=1, le=65535)
    heartbeat_interval_seconds: float = Field(default=30, gt=0)
    job_lease_seconds: float = Field(default=120, gt=0)

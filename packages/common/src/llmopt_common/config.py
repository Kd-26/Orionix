"""Environment-backed bootstrap configuration."""

from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class TelemetrySettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    enabled: bool = False


class BenchmarkingSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    output_dir: Path = Path("benchmark-output")


class OptimizationSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile: str = "default"


class Settings(BaseSettings):
    """Shared settings; secret values must be supplied externally."""

    model_config = SettingsConfigDict(
        env_prefix="LLMOPT_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    environment: Environment = Environment.DEVELOPMENT
    log_level: str = "INFO"
    log_format: str = "console"
    control_plane_url: str | None = None
    agent_id: str | None = None
    telemetry: TelemetrySettings = Field(default_factory=TelemetrySettings)
    benchmarking: BenchmarkingSettings = Field(default_factory=BenchmarkingSettings)
    optimization: OptimizationSettings = Field(default_factory=OptimizationSettings)

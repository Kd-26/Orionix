"""Typed configuration with explicit and testable source precedence."""

import os
import tomllib
from collections.abc import Mapping
from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class ControlPlaneSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: str | None = None


class AgentSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agent_id: str | None = None
    credential: SecretStr | None = None


class DatabaseSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: SecretStr | None = None


class StorageSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    root: Path = Path(".llmopt/storage")


class BenchmarkSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    output_dir: Path = Path("benchmark-output")


class OptimizerSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile: str = "default"


class TelemetrySettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    enabled: bool = False


class Settings(BaseSettings):
    """Process settings; nested environment names use ``__`` delimiters."""

    model_config = SettingsConfigDict(
        env_prefix="LLMOPT_",
        env_nested_delimiter="__",
        extra="forbid",
    )

    environment: Environment = Environment.DEVELOPMENT
    log_level: str = "INFO"
    log_format: str = "console"
    control_plane: ControlPlaneSettings = Field(default_factory=ControlPlaneSettings)
    agent: AgentSettings = Field(default_factory=AgentSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    benchmark: BenchmarkSettings = Field(default_factory=BenchmarkSettings)
    optimizer: OptimizerSettings = Field(default_factory=OptimizerSettings)
    telemetry: TelemetrySettings = Field(default_factory=TelemetrySettings)


def _deep_merge(base: dict[str, Any], overlay: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in overlay.items():
        current = merged.get(key)
        if isinstance(current, dict) and isinstance(value, Mapping):
            merged[key] = _deep_merge(current, value)
        else:
            merged[key] = value
    return merged


def load_settings(
    *,
    config_root: Path = Path("configs"),
    cli_overrides: Mapping[str, Any] | None = None,
) -> Settings:
    """Load defaults < environment TOML < environment variables < CLI values."""

    requested_environment = (
        cli_overrides.get("environment")
        if cli_overrides and "environment" in cli_overrides
        else os.getenv("LLMOPT_ENVIRONMENT", Environment.DEVELOPMENT)
    )
    if requested_environment is None:
        requested_environment = Environment.DEVELOPMENT
    environment = Environment(str(requested_environment))
    config_path = config_root / environment.value / "settings.toml"
    file_values: dict[str, Any] = {}
    if config_path.is_file():
        with config_path.open("rb") as config_file:
            file_values = tomllib.load(config_file)

    environment_settings = Settings()
    merged = _deep_merge(file_values, environment_settings.model_dump(exclude_unset=True))
    if cli_overrides:
        merged = _deep_merge(merged, cli_overrides)
    return Settings(**merged)

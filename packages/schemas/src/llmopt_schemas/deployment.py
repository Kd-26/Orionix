"""Provider-neutral deployment-export metadata."""

from enum import StrEnum
from typing import ClassVar

from pydantic import Field

from llmopt_schemas.base import ContractModel


class DeploymentFormat(StrEnum):
    ENV_FILE = "env_file"
    DOCKER_COMPOSE = "docker_compose"
    SHELL_ARGUMENTS = "shell_arguments"


class DeploymentExportMetadata(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    format: DeploymentFormat
    generated_files: tuple[str, ...] = ()
    required_secret_names: tuple[str, ...] = ()
    annotations: dict[str, str] = Field(default_factory=dict)

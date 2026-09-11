"""Provider-neutral execution, engine, and provisioning contracts."""

from datetime import datetime
from enum import StrEnum
from typing import ClassVar

from llmopt_common import AttemptId, JobId
from llmopt_domain import ComputeState
from pydantic import Field, JsonValue, model_validator

from llmopt_schemas.base import ContractModel
from llmopt_schemas.compatibility import CompatibilityFingerprint
from llmopt_schemas.model import ModelSpec
from llmopt_schemas.workload import WorkloadSpec


class ExecutionBackendKind(StrEnum):
    LOCAL_HOST = "local_host"
    DOCKER_HOST = "docker_host"
    RUNPOD = "runpod"
    JARVISLABS = "jarvislabs"
    MODAL = "modal"


class EngineEventType(StrEnum):
    STARTING = "starting"
    READY = "ready"
    LOG = "log"
    WARNING = "warning"
    STOPPED = "stopped"
    FAILED = "failed"


class ExecutionRequest(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    job_id: JobId
    attempt_id: AttemptId
    backend: ExecutionBackendKind
    model: ModelSpec
    workload: WorkloadSpec
    timeout_seconds: float = Field(gt=0)


class PreparedEnvironment(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    environment_id: str
    backend: ExecutionBackendKind
    fingerprint: CompatibilityFingerprint
    workspace_reference: str | None = None


class EngineLaunchSpec(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    executable: str
    argv: tuple[str, ...] = Field(min_length=1)
    container_image: str | None = None
    container_image_digest: str | None = None
    working_directory: str | None = None
    environment_variable_names: tuple[str, ...] = ()

    @model_validator(mode="after")
    def prohibit_shell_launches(self) -> "EngineLaunchSpec":
        executable_name = self.executable.rsplit("/", maxsplit=1)[-1].lower()
        if executable_name in {"bash", "cmd", "powershell", "pwsh", "sh", "zsh"}:
            raise ValueError("engine launch specifications cannot invoke a command shell")
        if not self.executable.strip() or any(not argument.strip() for argument in self.argv):
            raise ValueError("engine executable and arguments must be non-empty")
        return self


class ConfigValidationResult(ContractModel):
    valid: bool
    issues: tuple[str, ...] = ()


class EngineHandle(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    handle_id: str
    environment_id: str
    engine: str
    started_at: datetime
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class EngineEvent(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    event_type: EngineEventType
    occurred_at: datetime
    message: str | None = None
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class ProvisioningRequest(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    job_id: JobId
    backend: ExecutionBackendKind
    gpu_model: str | None = None
    gpu_count: int = Field(default=1, ge=1)
    region: str | None = None
    storage_bytes: int | None = Field(default=None, ge=0)
    maximum_cost_per_hour_usd: float | None = Field(default=None, ge=0)
    timeout_seconds: float = Field(gt=0)


class ComputeTarget(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    target_id: str
    backend: ExecutionBackendKind
    provider_resource_identifier_hash: str | None = None
    state: ComputeState
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class ComputeStatus(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    target_id: str
    state: ComputeState
    observed_at: datetime
    message: str | None = None

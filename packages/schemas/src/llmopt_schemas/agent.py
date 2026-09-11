"""Typed, allowlisted customer-agent protocol envelopes."""

from datetime import datetime
from enum import StrEnum
from typing import ClassVar

from llmopt_common import AgentId, AttemptId, JobId
from llmopt_domain import OptimizationJobState
from pydantic import Field, JsonValue, model_validator

from llmopt_schemas.base import ContractModel
from llmopt_schemas.execution import ExecutionBackendKind
from llmopt_schemas.hardware import HardwareSpec


class AgentCommandType(StrEnum):
    INSPECT = "inspect"
    PREPARE = "prepare"
    START_ENGINE = "start_engine"
    STOP_ENGINE = "stop_engine"
    RUN_BENCHMARK = "run_benchmark"
    CANCEL_JOB = "cancel_job"
    CLEANUP = "cleanup"
    COLLECT_DIAGNOSTICS = "collect_diagnostics"


class AgentCapabilities(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    agent_id: AgentId
    hardware: HardwareSpec | None = None
    execution_backends: tuple[ExecutionBackendKind, ...] = ()
    engines: tuple[str, ...] = ()


class AgentCommand(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    command_id: str
    command_type: AgentCommandType
    job_id: JobId
    attempt_id: AttemptId
    idempotency_key: str
    issued_at: datetime
    expires_at: datetime
    payload: dict[str, JsonValue] = Field(default_factory=dict)

    @model_validator(mode="after")
    def valid_window(self) -> "AgentCommand":
        if self.expires_at <= self.issued_at:
            raise ValueError("agent command must expire after it is issued")
        forbidden_keys = {"command", "script", "shell", "shell_command"}
        if forbidden_keys.intersection(key.lower() for key in self.payload):
            raise ValueError("agent commands cannot contain arbitrary shell payloads")
        return self


class JobStateTransition(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    job_id: JobId
    attempt_id: AttemptId
    previous_state: OptimizationJobState
    new_state: OptimizationJobState
    occurred_at: datetime
    sequence: int = Field(ge=0)
    reason: str | None = None

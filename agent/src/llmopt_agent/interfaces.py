"""Ports for future customer-side capabilities."""

from pathlib import Path
from typing import Protocol

from llmopt_capsule import ExecutionCapsuleManifest
from llmopt_common import CapsuleId, JobId
from llmopt_schemas import (
    AgentCapabilities,
    AgentCommand,
    DiagnosticBundleManifest,
    HardwareSpec,
    JobStateTransition,
    ModelSpec,
    ServingConfig,
    ValidationStatus,
)
from llmopt_telemetry import Metric


class EnvironmentInspector(Protocol):
    def inspect_hardware(self) -> HardwareSpec: ...

    def inspect_model(self, model_id: str, revision: str | None = None) -> ModelSpec: ...


class MetricsCollector(Protocol):
    def collect(self) -> tuple[Metric, ...]: ...


class CapsuleBuilder(Protocol):
    def build_manifest(self, capsule_id: CapsuleId) -> ExecutionCapsuleManifest: ...


class DeploymentValidator(Protocol):
    def validate(self, configuration: ServingConfig) -> ValidationStatus: ...


class HeartbeatPublisher(Protocol):
    async def publish(self, capabilities: AgentCapabilities) -> None: ...


class JobLeaseClient(Protocol):
    async def claim(self) -> AgentCommand | None: ...

    async def renew(self, command: AgentCommand) -> None: ...

    async def report_transition(self, transition: JobStateTransition) -> None: ...


class JobWorkspaceManager(Protocol):
    def create(self, job_id: JobId) -> Path: ...

    def cleanup(self, job_id: JobId) -> None: ...


class DiagnosticCollector(Protocol):
    def collect(self, job_id: JobId | None = None) -> DiagnosticBundleManifest: ...


class CommandHandler(Protocol):
    async def handle(self, command: AgentCommand) -> JobStateTransition: ...

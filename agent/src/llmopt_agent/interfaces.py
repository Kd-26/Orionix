"""Ports for future customer-side capabilities."""

from typing import Protocol

from llmopt_capsule import ExecutionCapsuleManifest
from llmopt_domain import CapsuleId
from llmopt_schemas import HardwareSpec, ModelSpec, ServingConfig, ValidationStatus
from llmopt_telemetry import Metric


class EnvironmentInspector(Protocol):
    def inspect_hardware(self) -> HardwareSpec: ...

    def inspect_model(self, model_id: str, revision: str | None = None) -> ModelSpec: ...


class EngineController(Protocol):
    def start(self, configuration: ServingConfig) -> None: ...

    def stop(self) -> None: ...


class MetricsCollector(Protocol):
    def collect(self) -> tuple[Metric, ...]: ...


class CapsuleBuilder(Protocol):
    def build_manifest(self, capsule_id: CapsuleId) -> ExecutionCapsuleManifest: ...


class DeploymentValidator(Protocol):
    def validate(self, configuration: ServingConfig) -> ValidationStatus: ...

"""Inspection ports implemented only at infrastructure edges."""

from typing import Protocol

from llmopt_schemas import HardwareSpec, ModelSpec


class InfrastructureInspector(Protocol):
    def inspect(self) -> HardwareSpec: ...


class ModelInspector(Protocol):
    def inspect(self, model_id: str, revision: str | None = None) -> ModelSpec: ...

"""Inference-engine adapter port that produces typed launch specifications."""

from typing import Protocol

from llmopt_schemas import HardwareSpec, ModelSpec, ServingConfig
from llmopt_schemas.execution import ConfigValidationResult, EngineLaunchSpec


class EngineAdapter(Protocol):
    def validate_config(
        self,
        model: ModelSpec,
        hardware: HardwareSpec,
        config: ServingConfig,
    ) -> ConfigValidationResult: ...

    def build_launch_spec(
        self,
        model: ModelSpec,
        config: ServingConfig,
    ) -> EngineLaunchSpec: ...

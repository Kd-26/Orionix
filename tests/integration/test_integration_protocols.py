"""Provider and engine ports remain implementable without vendor dependencies."""

import asyncio
import json
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from pathlib import Path

import pytest
from llmopt_domain import ComputeState
from llmopt_integrations import __version__
from llmopt_integrations.ports import EngineAdapter, ExecutionBackend, ProvisioningBackend
from llmopt_schemas import (
    ComputeStatus,
    ComputeTarget,
    ConfigValidationResult,
    EngineEvent,
    EngineHandle,
    EngineLaunchSpec,
    HardwareSpec,
    ModelSpec,
    PreparedEnvironment,
    ProvisioningRequest,
    ServingConfig,
)
from llmopt_schemas.execution import ExecutionRequest

FIXTURES = Path(__file__).parents[1] / "fixtures" / "contracts" / "v1"


def _load_contract(name: str) -> dict[str, object]:
    payload: object = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


class StubEngineAdapter:
    def validate_config(
        self,
        model: ModelSpec,
        hardware: HardwareSpec,
        config: ServingConfig,
    ) -> ConfigValidationResult:
        del model, hardware, config
        return ConfigValidationResult(valid=True)

    def build_launch_spec(
        self,
        model: ModelSpec,
        config: ServingConfig,
    ) -> EngineLaunchSpec:
        del model, config
        return EngineLaunchSpec(schema_version="1.0", executable="engine", argv=("serve",))


class StubExecutionBackend:
    async def inspect(self) -> HardwareSpec:
        return HardwareSpec.model_validate(_load_contract("hardware.json"))

    async def prepare(self, request: ExecutionRequest) -> PreparedEnvironment:
        raise NotImplementedError(request)

    async def start_engine(
        self,
        environment: PreparedEnvironment,
        config: ServingConfig,
    ) -> EngineHandle:
        raise NotImplementedError(environment, config)

    async def stream_events(self, handle: EngineHandle) -> AsyncIterator[EngineEvent]:
        if False:
            yield EngineEvent(
                schema_version="1.0", occurred_at=datetime.now(UTC), event_type="ready"
            )
        del handle

    async def stop_engine(self, handle: EngineHandle) -> None:
        del handle

    async def cleanup(self, environment: PreparedEnvironment) -> None:
        del environment


class StubProvisioningBackend:
    async def provision(self, request: ProvisioningRequest) -> ComputeTarget:
        return ComputeTarget(
            schema_version="1.0",
            target_id=str(request.job_id),
            backend=request.backend,
            state=ComputeState.READY,
        )

    async def status(self, target: ComputeTarget) -> ComputeStatus:
        return ComputeStatus(
            schema_version="1.0",
            target_id=target.target_id,
            state=target.state,
            observed_at=datetime.now(UTC),
        )

    async def terminate(self, target: ComputeTarget) -> None:
        del target


engine_adapter: EngineAdapter = StubEngineAdapter()
execution_backend: ExecutionBackend = StubExecutionBackend()
provisioning_backend: ProvisioningBackend = StubProvisioningBackend()


@pytest.mark.integration
def test_engine_port_accepts_a_trivial_double() -> None:
    result = engine_adapter.validate_config(
        ModelSpec.model_validate(_load_contract("model.json")),
        HardwareSpec.model_validate(_load_contract("hardware.json")),
        ServingConfig(schema_version="1.0", engine="stub"),
    )

    assert result.valid
    assert __version__ == "0.1.0.dev0"


@pytest.mark.integration
def test_execution_port_accepts_a_trivial_double() -> None:
    assert asyncio.run(execution_backend.inspect()).cluster.accelerator_count == 0

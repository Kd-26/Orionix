"""Execution backend port shared by persistent and serverless targets."""

from collections.abc import AsyncIterator
from typing import Protocol

from llmopt_schemas import HardwareSpec, ServingConfig
from llmopt_schemas.execution import (
    EngineEvent,
    EngineHandle,
    ExecutionRequest,
    PreparedEnvironment,
)


class ExecutionBackend(Protocol):
    async def inspect(self) -> HardwareSpec: ...

    async def prepare(self, request: ExecutionRequest) -> PreparedEnvironment: ...

    async def start_engine(
        self,
        environment: PreparedEnvironment,
        config: ServingConfig,
    ) -> EngineHandle: ...

    def stream_events(self, handle: EngineHandle) -> AsyncIterator[EngineEvent]: ...

    async def stop_engine(self, handle: EngineHandle) -> None: ...

    async def cleanup(self, environment: PreparedEnvironment) -> None: ...

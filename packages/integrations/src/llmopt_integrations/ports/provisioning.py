"""Separate cloud/provider provisioning port."""

from typing import Protocol

from llmopt_schemas.execution import ComputeStatus, ComputeTarget, ProvisioningRequest


class ProvisioningBackend(Protocol):
    async def provision(self, request: ProvisioningRequest) -> ComputeTarget: ...

    async def status(self, target: ComputeTarget) -> ComputeStatus: ...

    async def terminate(self, target: ComputeTarget) -> None: ...

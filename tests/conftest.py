"""Shared test policy, including automatic GPU-test skipping."""

import importlib.util
from typing import Protocol, cast

import pytest


class _CudaModule(Protocol):
    def is_available(self) -> bool: ...


class _TorchModule(Protocol):
    cuda: _CudaModule


def _cuda_available() -> bool:
    if importlib.util.find_spec("torch") is None:
        return False
    torch = cast("_TorchModule", importlib.import_module("torch"))
    return bool(torch.cuda.is_available())


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    if _cuda_available():
        return
    skip_gpu = pytest.mark.skip(reason="CUDA-capable hardware is unavailable")
    for item in items:
        if "gpu" in item.keywords:
            item.add_marker(skip_gpu)

"""Workload loading boundary without analysis or traffic capture."""

from pathlib import Path
from typing import Protocol

from llmopt_schemas import WorkloadSpec


class WorkloadLoader(Protocol):
    def load(self, source: Path) -> WorkloadSpec: ...

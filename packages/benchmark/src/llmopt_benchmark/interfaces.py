"""Execution port implemented later by customer-side adapters."""

from typing import Protocol

from llmopt_schemas import BenchmarkResult

from llmopt_benchmark.contracts import BenchmarkRun


class BenchmarkRunner(Protocol):
    def run(self, benchmark: BenchmarkRun) -> tuple[BenchmarkResult, ...]: ...

"""Narrow optimizer ports; concrete algorithms are deferred."""

from dataclasses import dataclass
from typing import Protocol

from llmopt_schemas import (
    BenchmarkResult,
    HardwareSpec,
    ModelSpec,
    ServingConfig,
    SLOSpec,
    WorkloadSpec,
)


@dataclass(frozen=True, slots=True)
class OptimizationContext:
    model: ModelSpec
    hardware: HardwareSpec
    workload: WorkloadSpec
    slo: SLOSpec


class CapabilityEvaluator(Protocol):
    def accepts(self, context: OptimizationContext, config: ServingConfig) -> bool: ...


class CandidateGenerator(Protocol):
    def generate(self, context: OptimizationContext) -> tuple[ServingConfig, ...]: ...


class OptimizationStrategy(Protocol):
    def propose(
        self,
        context: OptimizationContext,
        observed: tuple[BenchmarkResult, ...],
    ) -> tuple[ServingConfig, ...]: ...


class ConstraintEvaluator(Protocol):
    def accepts(self, result: BenchmarkResult, slo: SLOSpec) -> bool: ...


class ResultRanker(Protocol):
    def rank(self, results: tuple[BenchmarkResult, ...]) -> tuple[BenchmarkResult, ...]: ...

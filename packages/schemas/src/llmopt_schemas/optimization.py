"""Optimization outcome contract; contains no ranking logic."""

from enum import StrEnum

from llmopt_domain import ConfigurationId
from pydantic import Field

from llmopt_schemas.base import ContractModel
from llmopt_schemas.benchmark import BenchmarkResult


class ValidationStatus(StrEnum):
    NOT_VALIDATED = "not_validated"
    PASSED = "passed"
    FAILED = "failed"


class OptimizationResult(ContractModel):
    baseline: BenchmarkResult | None = None
    candidate_results: tuple[BenchmarkResult, ...] = ()
    pareto_candidates: tuple[ConfigurationId, ...] = ()
    recommended_profile: ConfigurationId | None = None
    reasoning_metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)
    constraints: tuple[str, ...] = ()
    validation_status: ValidationStatus = ValidationStatus.NOT_VALIDATED

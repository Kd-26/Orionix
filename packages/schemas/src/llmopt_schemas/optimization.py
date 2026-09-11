"""Optimization outcome contract; contains no ranking logic."""

from enum import StrEnum
from typing import ClassVar

from llmopt_common import ConfigurationId, JobId
from pydantic import Field

from llmopt_schemas.base import ContractModel
from llmopt_schemas.benchmark import BenchmarkResult
from llmopt_schemas.hardware import HardwareSpec
from llmopt_schemas.model import ModelSpec
from llmopt_schemas.quality import QualityConstraint
from llmopt_schemas.serving import ServingConfig
from llmopt_schemas.slo import SLOSpec
from llmopt_schemas.workload import WorkloadSpec


class ValidationStatus(StrEnum):
    NOT_VALIDATED = "not_validated"
    PASSED = "passed"
    FAILED = "failed"


class CandidateEvaluation(ContractModel):
    configuration_id: ConfigurationId
    configuration: ServingConfig
    benchmark: BenchmarkResult | None = None
    quality_loss: float | None = Field(default=None, ge=0)
    satisfied_constraints: tuple[str, ...] = ()
    rejected_reasons: tuple[str, ...] = ()


class OptimizationRequest(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    job_id: JobId
    model: ModelSpec
    hardware: HardwareSpec
    workload: WorkloadSpec
    slo: SLOSpec
    quality_constraints: tuple[QualityConstraint, ...] = ()
    maximum_candidates: int = Field(default=32, ge=1)
    maximum_search_seconds: float | None = Field(default=None, gt=0)


class OptimizationResult(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    job_id: JobId | None = None
    baseline: BenchmarkResult | None = None
    candidate_results: tuple[CandidateEvaluation, ...] = ()
    pareto_candidates: tuple[ConfigurationId, ...] = ()
    recommended_profile: ConfigurationId | None = None
    reasoning_metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)
    constraints: tuple[str, ...] = ()
    validation_status: ValidationStatus = ValidationStatus.NOT_VALIDATED

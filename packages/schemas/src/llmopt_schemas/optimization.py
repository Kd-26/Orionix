"""Versioned optimization request, job, candidate, and recommendation contracts."""

from datetime import datetime
from enum import StrEnum
from typing import ClassVar

from llmopt_common import (
    BenchmarkRunId,
    ConfigurationId,
    JobId,
    OrganizationId,
    ProjectId,
)
from llmopt_domain import OptimizationJobState
from pydantic import Field, model_validator

from llmopt_schemas.base import ContractModel
from llmopt_schemas.benchmark import BenchmarkResult
from llmopt_schemas.compatibility import CompatibilityFingerprint
from llmopt_schemas.hardware import HardwareSpec
from llmopt_schemas.model import ModelSpec
from llmopt_schemas.requirements import OptimizationRequirements
from llmopt_schemas.serving import ServingConfig
from llmopt_schemas.workload import WorkloadSpec


class ValidationStatus(StrEnum):
    NOT_VALIDATED = "not_validated"
    PASSED = "passed"
    FAILED = "failed"


class CandidateConfiguration(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    configuration_id: ConfigurationId
    configuration: ServingConfig
    generation_reason: str = Field(min_length=1)
    required_capabilities: tuple[str, ...] = ()
    compatibility: CompatibilityFingerprint | None = None


class CandidateEvaluation(ContractModel):
    candidate: CandidateConfiguration
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
    requirements: OptimizationRequirements


class JobOwner(ContractModel):
    organization_id: OrganizationId
    project_id: ProjectId
    principal_identifier_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$")


class OptimizationJobSpec(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    job_id: JobId
    owner: JobOwner
    request: OptimizationRequest
    state: OptimizationJobState
    created_at: datetime
    updated_at: datetime

    @model_validator(mode="after")
    def validate_job_identity_and_timestamps(self) -> "OptimizationJobSpec":
        if self.request.job_id != self.job_id:
            raise ValueError("job and request identifiers must match")
        if self.updated_at < self.created_at:
            raise ValueError("job update time cannot precede creation time")
        return self


class Recommendation(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    job_id: JobId
    winning_configuration_id: ConfigurationId
    alternative_configuration_ids: tuple[ConfigurationId, ...] = ()
    evidence_run_ids: tuple[BenchmarkRunId, ...] = Field(min_length=1)
    explanation: str = Field(min_length=1)
    warnings: tuple[str, ...] = ()

    @model_validator(mode="after")
    def winner_is_not_an_alternative(self) -> "Recommendation":
        if self.winning_configuration_id in self.alternative_configuration_ids:
            raise ValueError("winning configuration cannot also be an alternative")
        return self


class OptimizationResult(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    job_id: JobId
    baseline: BenchmarkResult | None = None
    candidate_results: tuple[CandidateEvaluation, ...] = ()
    pareto_candidates: tuple[ConfigurationId, ...] = ()
    recommendation: Recommendation | None = None
    reasoning_metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)
    constraints: tuple[str, ...] = ()
    validation_status: ValidationStatus = ValidationStatus.NOT_VALIDATED

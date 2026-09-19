"""Optimization objectives, constraints, and hard experiment budgets."""

from enum import StrEnum
from typing import ClassVar

from pydantic import Field, model_validator

from llmopt_schemas.base import ContractModel
from llmopt_schemas.quality import QualityConstraint
from llmopt_schemas.slo import SLOSpec


class ObjectiveIdentifier(StrEnum):
    MAXIMIZE_GOODPUT = "MAXIMIZE_GOODPUT"
    MAXIMIZE_THROUGHPUT = "MAXIMIZE_THROUGHPUT"
    MINIMIZE_TTFT = "MINIMIZE_TTFT"
    MINIMIZE_TPOT = "MINIMIZE_TPOT"
    MINIMIZE_COST_PER_TOKEN = "MINIMIZE_COST_PER_TOKEN"
    BALANCED_WITH_EXPLICIT_WEIGHTS = "BALANCED_WITH_EXPLICIT_WEIGHTS"


class OptimizationObjective(ContractModel):
    identifier: ObjectiveIdentifier = ObjectiveIdentifier.MAXIMIZE_GOODPUT
    weights: dict[ObjectiveIdentifier, float] = Field(default_factory=dict)

    @model_validator(mode="after")
    def explicit_balanced_weights(self) -> "OptimizationObjective":
        if self.identifier is ObjectiveIdentifier.BALANCED_WITH_EXPLICIT_WEIGHTS:
            if not self.weights or any(weight <= 0 for weight in self.weights.values()):
                raise ValueError("balanced objectives require explicit positive weights")
        elif self.weights:
            raise ValueError("weights are only valid for the balanced objective")
        return self


class ExperimentBudget(ContractModel):
    maximum_candidates: int = Field(ge=1)
    maximum_elapsed_seconds: float = Field(gt=0)
    maximum_gpu_hours: float = Field(gt=0)
    maximum_cost_usd: float | None = Field(default=None, ge=0)
    maximum_consecutive_oom_candidates: int = Field(default=2, ge=0)
    maximum_repeated_infrastructure_failures: int = Field(default=3, ge=0)
    minimum_finalist_confirmation_runs: int = Field(default=2, ge=1)


class OptimizationRequirements(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    objective: OptimizationObjective = Field(default_factory=OptimizationObjective)
    slo: SLOSpec
    quality_constraints: tuple[QualityConstraint, ...] = ()
    experiment_budget: ExperimentBudget

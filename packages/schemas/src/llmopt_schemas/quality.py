"""Quality-validation contracts; no inference or evaluator implementation."""

from enum import StrEnum
from typing import ClassVar

from pydantic import Field

from llmopt_schemas.base import ContractModel


class QualityMetric(StrEnum):
    EXACT_MATCH = "exact_match"
    NORMALIZED_MATCH = "normalized_match"
    STRUCTURED_OUTPUT_VALIDITY = "structured_output_validity"
    SEMANTIC_COMPARISON = "semantic_comparison"


class EvaluationDatasetRef(ContractModel):
    dataset_id: str
    version: str
    content_hash: str
    customer_side_path: str | None = None


class QualityConstraint(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    metric: QualityMetric
    maximum_loss: float = Field(ge=0)
    evaluator_version_fingerprint: str
    dataset: EvaluationDatasetRef


class QualityEvaluation(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    metric: QualityMetric
    baseline_score: float
    candidate_score: float
    quality_loss: float = Field(ge=0)
    evaluator_version_fingerprint: str
    dataset: EvaluationDatasetRef

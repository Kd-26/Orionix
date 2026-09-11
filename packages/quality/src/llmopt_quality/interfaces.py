"""Quality evaluator port; raw outputs remain customer-side."""

from typing import Protocol

from llmopt_schemas.quality import QualityConstraint, QualityEvaluation


class QualityEvaluator(Protocol):
    def evaluate(self, constraint: QualityConstraint) -> QualityEvaluation: ...

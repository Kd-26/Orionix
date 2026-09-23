"""Optimization interfaces and deterministic pre-execution filtering."""

from llmopt_optimizer.compatibility import CandidateCompatibilityEvaluator
from llmopt_optimizer.interfaces import (
    CandidateGenerator,
    CapabilityEvaluator,
    ConstraintEvaluator,
    OptimizationContext,
    OptimizationStrategy,
    ResultRanker,
)

__all__ = [
    "CandidateCompatibilityEvaluator",
    "CandidateGenerator",
    "CapabilityEvaluator",
    "ConstraintEvaluator",
    "OptimizationContext",
    "OptimizationStrategy",
    "ResultRanker",
]

__version__ = "0.1.0.dev0"

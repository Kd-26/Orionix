"""Optimization interfaces without algorithms."""

from llmopt_optimizer.interfaces import (
    CandidateGenerator,
    ConstraintEvaluator,
    OptimizationContext,
    OptimizationStrategy,
    ResultRanker,
)

__all__ = [
    "CandidateGenerator",
    "ConstraintEvaluator",
    "OptimizationContext",
    "OptimizationStrategy",
    "ResultRanker",
]

__version__ = "0.1.0.dev0"

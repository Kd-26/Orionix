"""Optimization interfaces without algorithms."""

from llmopt_optimizer.interfaces import (
    CandidateGenerator,
    CapabilityEvaluator,
    ConstraintEvaluator,
    OptimizationContext,
    OptimizationStrategy,
    ResultRanker,
)

__all__ = [
    "CandidateGenerator",
    "CapabilityEvaluator",
    "ConstraintEvaluator",
    "OptimizationContext",
    "OptimizationStrategy",
    "ResultRanker",
]

__version__ = "0.1.0.dev0"

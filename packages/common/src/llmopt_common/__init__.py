"""Shared foundations with no product algorithms."""

from llmopt_common.config import Environment, Settings
from llmopt_common.errors import (
    BenchmarkError,
    CapsuleError,
    CompatibilityError,
    ConfigurationError,
    IntegrationError,
    LlmOptError,
    OptimizationError,
)

__all__ = [
    "BenchmarkError",
    "CapsuleError",
    "CompatibilityError",
    "ConfigurationError",
    "Environment",
    "IntegrationError",
    "LlmOptError",
    "OptimizationError",
    "Settings",
]

__version__ = "0.1.0.dev0"

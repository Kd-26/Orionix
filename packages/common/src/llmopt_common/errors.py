"""Minimal shared exception hierarchy."""


class LlmOptError(Exception):
    """Base exception for expected Orionix failures."""


class ConfigurationError(LlmOptError):
    """Configuration is missing or invalid."""


class CompatibilityError(LlmOptError):
    """Components or artifacts are incompatible."""


class IntegrationError(LlmOptError):
    """An external engine or provider integration failed."""


class BenchmarkError(LlmOptError):
    """Benchmark planning or execution failed."""


class OptimizationError(LlmOptError):
    """Optimization planning or evaluation failed."""


class CapsuleError(LlmOptError):
    """Execution Capsule metadata or lifecycle operation failed."""

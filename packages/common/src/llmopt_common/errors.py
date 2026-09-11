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


class ExecutionError(LlmOptError):
    """A provider-neutral execution operation failed."""


class ProvisioningError(LlmOptError):
    """A compute provisioning operation failed."""


class QualityError(LlmOptError):
    """Quality validation failed or could not be completed."""


class DeploymentExportError(LlmOptError):
    """Deployment configuration export failed."""

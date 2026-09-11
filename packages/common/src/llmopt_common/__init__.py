"""Shared foundations with no product algorithms."""

from llmopt_common.errors import (
    BenchmarkError,
    CapsuleError,
    CompatibilityError,
    ConfigurationError,
    DeploymentExportError,
    ExecutionError,
    IntegrationError,
    LlmOptError,
    OptimizationError,
    ProvisioningError,
    QualityError,
)
from llmopt_common.identifiers import (
    AgentId,
    AttemptId,
    BenchmarkRunId,
    CapsuleId,
    ConfigurationId,
    ExperimentId,
    JobId,
    OptimizationJobId,
    OrganizationId,
    ProjectId,
    ScheduleId,
)

__all__ = [
    "AgentId",
    "AttemptId",
    "BenchmarkError",
    "BenchmarkRunId",
    "CapsuleError",
    "CapsuleId",
    "CompatibilityError",
    "ConfigurationError",
    "ConfigurationId",
    "DeploymentExportError",
    "ExecutionError",
    "ExperimentId",
    "IntegrationError",
    "JobId",
    "LlmOptError",
    "OptimizationError",
    "OptimizationJobId",
    "OrganizationId",
    "ProjectId",
    "ProvisioningError",
    "QualityError",
    "ScheduleId",
]

__version__ = "0.1.0.dev0"

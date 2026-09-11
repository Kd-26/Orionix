"""Dependency-free domain primitives."""

from llmopt_domain.enums import CapsuleState, OptimizationJobState
from llmopt_domain.identifiers import (
    BenchmarkRunId,
    CapsuleId,
    ConfigurationId,
    OptimizationJobId,
    OrganizationId,
    ProjectId,
)

__all__ = [
    "BenchmarkRunId",
    "CapsuleId",
    "CapsuleState",
    "ConfigurationId",
    "OptimizationJobId",
    "OptimizationJobState",
    "OrganizationId",
    "ProjectId",
]

__version__ = "0.1.0.dev0"

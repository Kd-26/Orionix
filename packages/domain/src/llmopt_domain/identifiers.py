"""Strongly typed UUID identifiers without persistence assumptions."""

from typing import NewType
from uuid import UUID

OrganizationId = NewType("OrganizationId", UUID)
ProjectId = NewType("ProjectId", UUID)
OptimizationJobId = NewType("OptimizationJobId", UUID)
BenchmarkRunId = NewType("BenchmarkRunId", UUID)
ConfigurationId = NewType("ConfigurationId", UUID)
CapsuleId = NewType("CapsuleId", UUID)

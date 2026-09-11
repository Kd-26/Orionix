"""Strongly typed UUID identifiers shared across subsystem boundaries."""

from typing import NewType
from uuid import UUID

OrganizationId = NewType("OrganizationId", UUID)
ProjectId = NewType("ProjectId", UUID)
AgentId = NewType("AgentId", UUID)
JobId = NewType("JobId", UUID)
OptimizationJobId = NewType("OptimizationJobId", UUID)
AttemptId = NewType("AttemptId", UUID)
ExperimentId = NewType("ExperimentId", UUID)
BenchmarkRunId = NewType("BenchmarkRunId", UUID)
ConfigurationId = NewType("ConfigurationId", UUID)
CapsuleId = NewType("CapsuleId", UUID)
ScheduleId = NewType("ScheduleId", UUID)

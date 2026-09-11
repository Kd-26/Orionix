"""Transport-neutral control-plane resource contracts; no persistence or API."""

from datetime import datetime
from enum import StrEnum
from typing import ClassVar

from llmopt_common import (
    AgentId,
    AttemptId,
    BenchmarkRunId,
    CapsuleId,
    ExperimentId,
    JobId,
    OrganizationId,
    ProjectId,
    ScheduleId,
)
from llmopt_domain import CapsuleState, OptimizationJobState
from pydantic import Field, JsonValue

from llmopt_schemas.base import ContractModel


class MembershipRole(StrEnum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class ControlPlaneContract(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION


class Organization(ControlPlaneContract):
    organization_id: OrganizationId
    name: str


class Membership(ControlPlaneContract):
    membership_id: str
    organization_id: OrganizationId
    principal_identifier_hash: str
    role: MembershipRole


class Project(ControlPlaneContract):
    project_id: ProjectId
    organization_id: OrganizationId
    name: str


class AgentRecord(ControlPlaneContract):
    agent_id: AgentId
    project_id: ProjectId
    version: str
    last_heartbeat_at: datetime | None = None


class OptimizationJobRecord(ControlPlaneContract):
    job_id: JobId
    project_id: ProjectId
    state: OptimizationJobState
    created_at: datetime


class OptimizationAttempt(ControlPlaneContract):
    attempt_id: AttemptId
    job_id: JobId
    sequence: int = Field(ge=1)
    state: OptimizationJobState
    created_at: datetime


class Experiment(ControlPlaneContract):
    experiment_id: ExperimentId
    job_id: JobId
    benchmark_runs: tuple[BenchmarkRunId, ...] = ()


class CapsuleMetadata(ControlPlaneContract):
    capsule_id: CapsuleId
    project_id: ProjectId
    state: CapsuleState
    manifest_digest: str


class RevalidationSchedule(ControlPlaneContract):
    schedule_id: ScheduleId
    project_id: ProjectId
    interval_seconds: int = Field(gt=0)
    enabled: bool = True
    manual_approval_required: bool = True


class AuditEvent(ControlPlaneContract):
    event_id: str
    organization_id: OrganizationId
    project_id: ProjectId | None = None
    actor_identifier_hash: str
    action: str
    resource_type: str
    resource_identifier_hash: str
    occurred_at: datetime
    metadata: dict[str, JsonValue] = Field(default_factory=dict)

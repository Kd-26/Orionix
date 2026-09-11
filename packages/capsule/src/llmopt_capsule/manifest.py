"""Versioned metadata schema; no artifact loading or integrity implementation."""

from datetime import datetime
from typing import ClassVar

from llmopt_domain import CapsuleId, CapsuleState
from llmopt_schemas import CompatibilityFingerprint, ServingConfig
from llmopt_schemas.base import ContractModel
from pydantic import Field


class ArtifactDescriptor(ContractModel):
    kind: str
    relative_path: str
    media_type: str | None = None
    size_bytes: int | None = Field(default=None, ge=0)
    digest: str | None = None


class IntegrityMetadata(ContractModel):
    algorithm: str | None = None
    manifest_digest: str | None = None
    signature: str | None = None
    signer: str | None = None


class ExecutionCapsuleManifest(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    capsule_id: CapsuleId
    state: CapsuleState = CapsuleState.CREATED
    created_at: datetime
    compatibility: CompatibilityFingerprint
    serving_configuration: ServingConfig
    engine_metadata: dict[str, str] = Field(default_factory=dict)
    compilation_artifacts: tuple[ArtifactDescriptor, ...] = ()
    graph_artifacts: tuple[ArtifactDescriptor, ...] = ()
    memory_layout: dict[str, str | int] = Field(default_factory=dict)
    scheduler_policy: dict[str, str | int | float | bool] = Field(default_factory=dict)
    cache_policy: dict[str, str | int | float | bool] = Field(default_factory=dict)
    integrity: IntegrityMetadata = Field(default_factory=IntegrityMetadata)

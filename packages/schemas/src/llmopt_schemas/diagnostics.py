"""Redaction-aware diagnostic bundle metadata."""

from datetime import datetime
from typing import ClassVar

from llmopt_common import AgentId, JobId
from pydantic import Field

from llmopt_schemas.base import ContractModel


class DiagnosticFile(ContractModel):
    relative_path: str
    media_type: str
    size_bytes: int = Field(ge=0)
    digest: str
    redacted: bool


class DiagnosticBundleManifest(ContractModel):
    SCHEMA_VERSION: ClassVar[str] = "1.0"

    schema_version: str = SCHEMA_VERSION
    bundle_id: str
    agent_id: AgentId
    job_id: JobId | None = None
    created_at: datetime
    files: tuple[DiagnosticFile, ...] = ()
    preview_required_before_upload: bool = True

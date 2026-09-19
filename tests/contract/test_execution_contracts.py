"""Execution envelopes reject unsafe or ambiguous values."""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from llmopt_common import AttemptId, JobId
from llmopt_schemas import (
    AgentCommand,
    AgentCommandType,
    EngineLaunchSpec,
)
from pydantic import ValidationError


@pytest.mark.contract
def test_engine_launch_spec_requires_typed_arguments() -> None:
    with pytest.raises(ValidationError):
        EngineLaunchSpec(schema_version="1.0", executable="vllm", argv=())

    with pytest.raises(ValidationError):
        EngineLaunchSpec(
            schema_version="1.0", executable="/bin/sh", argv=("-c", "arbitrary command")
        )


@pytest.mark.contract
def test_agent_command_is_allowlisted_and_time_bounded() -> None:
    issued_at = datetime.now(UTC)
    command = AgentCommand(
        schema_version="1.0",
        command_id="command-1",
        command_type=AgentCommandType.INSPECT,
        job_id=JobId(uuid4()),
        attempt_id=AttemptId(uuid4()),
        idempotency_key="inspect-once",
        issued_at=issued_at,
        expires_at=issued_at + timedelta(minutes=5),
    )

    assert command.command_type is AgentCommandType.INSPECT


@pytest.mark.contract
def test_agent_command_rejects_invalid_expiration() -> None:
    now = datetime.now(UTC)
    with pytest.raises(ValidationError):
        AgentCommand(
            schema_version="1.0",
            command_id="command-1",
            command_type=AgentCommandType.CLEANUP,
            job_id=JobId(uuid4()),
            attempt_id=AttemptId(uuid4()),
            idempotency_key="cleanup-once",
            issued_at=now,
            expires_at=now,
        )


@pytest.mark.contract
def test_agent_command_rejects_shell_payloads() -> None:
    now = datetime.now(UTC)
    with pytest.raises(ValidationError):
        AgentCommand(
            schema_version="1.0",
            command_id="command-1",
            command_type=AgentCommandType.START_ENGINE,
            job_id=JobId(uuid4()),
            attempt_id=AttemptId(uuid4()),
            idempotency_key="start-once",
            issued_at=now,
            expires_at=now + timedelta(minutes=5),
            payload={"shell": "rm -rf /"},
        )

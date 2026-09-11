"""Safe, structured-logging-ready standard-library configuration."""

import json
import logging
import re
from collections.abc import Mapping
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Any

correlation_id: ContextVar[str | None] = ContextVar("correlation_id", default=None)
organization_id: ContextVar[str | None] = ContextVar("organization_id", default=None)
project_id: ContextVar[str | None] = ContextVar("project_id", default=None)
job_id: ContextVar[str | None] = ContextVar("job_id", default=None)
attempt_id: ContextVar[str | None] = ContextVar("attempt_id", default=None)
run_id: ContextVar[str | None] = ContextVar("run_id", default=None)
agent_id: ContextVar[str | None] = ContextVar("agent_id", default=None)

_SECRET_PATTERN = re.compile(
    r"(?i)(token|password|secret|api[_-]?key|authorization)\s*[:=]\s*([^\s,;]+)"
)


def redact_text(value: str) -> str:
    """Redact common credential assignments from an already-safe log message."""

    return _SECRET_PATTERN.sub(r"\1=[REDACTED]", value)


class JsonFormatter(logging.Formatter):
    """Emit a deliberately small JSON record without arbitrary record fields."""

    def format(self, record: logging.LogRecord) -> str:
        payload: Mapping[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": redact_text(record.getMessage()),
            "correlation_id": correlation_id.get(),
            "organization_id": organization_id.get(),
            "project_id": project_id.get(),
            "job_id": job_id.get(),
            "attempt_id": attempt_id.get(),
            "run_id": run_id.get(),
            "agent_id": agent_id.get(),
        }
        return json.dumps(payload, separators=(",", ":"))


def configure_logging(*, level: str = "INFO", json_output: bool = False) -> None:
    """Configure process logging without exporting data or adding sensitive fields."""

    handler = logging.StreamHandler()
    if json_output:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter("%(levelname)s %(name)s %(message)s"))
        handler.addFilter(_RedactingFilter())
    logging.basicConfig(level=level.upper(), handlers=[handler], force=True)


class _RedactingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = redact_text(record.getMessage())
        record.args = ()
        return True

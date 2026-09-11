"""Safe, structured-logging-ready standard-library configuration."""

import json
import logging
from collections.abc import Mapping
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Any

correlation_id: ContextVar[str | None] = ContextVar("correlation_id", default=None)
job_id: ContextVar[str | None] = ContextVar("job_id", default=None)


class JsonFormatter(logging.Formatter):
    """Emit a deliberately small JSON record without arbitrary record fields."""

    def format(self, record: logging.LogRecord) -> str:
        payload: Mapping[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": correlation_id.get(),
            "job_id": job_id.get(),
        }
        return json.dumps(payload, separators=(",", ":"))


def configure_logging(*, level: str = "INFO", json_output: bool = False) -> None:
    """Configure process logging without exporting data or adding sensitive fields."""

    handler = logging.StreamHandler()
    if json_output:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter("%(levelname)s %(name)s %(message)s"))
    logging.basicConfig(level=level.upper(), handlers=[handler], force=True)

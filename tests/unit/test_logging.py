"""Logging bootstrap supports console and structured modes."""

import logging

import pytest
from llmopt_common.logging import JsonFormatter, configure_logging, redact_text


@pytest.mark.unit
def test_json_formatter_uses_allow_list() -> None:
    formatter = JsonFormatter()
    record = logging.LogRecord("test", logging.INFO, __file__, 1, "safe", (), None)

    output = formatter.format(record)

    assert '"message":"safe"' in output


@pytest.mark.unit
def test_logging_configuration_starts() -> None:
    configure_logging(level="INFO", json_output=False)


@pytest.mark.unit
def test_common_credential_shapes_are_redacted() -> None:
    assert redact_text("api_key=super-secret") == "api_key=[REDACTED]"

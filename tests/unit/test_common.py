"""Common identifiers and errors have one consistent convention."""

from uuid import uuid4

import pytest
from llmopt_common import AgentId, ConfigurationError, JobId, LlmOptError


@pytest.mark.unit
def test_identifiers_preserve_uuid_values_and_static_distinction() -> None:
    value = uuid4()

    assert AgentId(value) == value
    assert JobId(value) == value


@pytest.mark.unit
def test_common_errors_share_one_base() -> None:
    assert issubclass(ConfigurationError, LlmOptError)

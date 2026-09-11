"""Configuration defaults are safe for CPU-only local development."""

import pytest
from llmopt_common import Environment, Settings


@pytest.mark.unit
def test_configuration_loads_safe_defaults() -> None:
    settings = Settings()

    assert settings.environment is Environment.DEVELOPMENT
    assert settings.telemetry.enabled is False
    assert settings.control_plane_url is None

"""Configuration precedence and secret representation are safe."""

from pathlib import Path

import pytest
from llmopt_config import Environment, Settings, load_settings


@pytest.mark.unit
def test_configuration_loads_safe_defaults() -> None:
    settings = Settings()

    assert settings.environment is Environment.DEVELOPMENT
    assert settings.telemetry.enabled is False
    assert settings.control_plane.url is None


@pytest.mark.unit
def test_configuration_precedence_and_secret_redaction(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_dir = tmp_path / "testing"
    config_dir.mkdir()
    (config_dir / "settings.toml").write_text(
        'environment = "testing"\n[telemetry]\nenabled = false\n',
        encoding="utf-8",
    )
    monkeypatch.setenv("LLMOPT_ENVIRONMENT", "testing")
    monkeypatch.setenv("LLMOPT_TELEMETRY__ENABLED", "true")
    monkeypatch.setenv("LLMOPT_AGENT__CREDENTIAL", "top-secret")

    settings = load_settings(
        config_root=tmp_path,
        cli_overrides={"telemetry": {"enabled": False}},
    )

    assert settings.environment is Environment.TESTING
    assert settings.telemetry.enabled is False
    assert "top-secret" not in repr(settings)
    assert "**********" in repr(settings)

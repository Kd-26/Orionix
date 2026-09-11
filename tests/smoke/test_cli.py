"""CLI help and placeholder commands remain executable."""

import pytest
from llmopt_cli.main import app
from typer.testing import CliRunner

runner = CliRunner()


@pytest.mark.smoke
def test_root_help() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "optimize" in result.output


@pytest.mark.smoke
def test_optimize_help() -> None:
    result = runner.invoke(app, ["optimize", "--help"])

    assert result.exit_code == 0
    assert "placeholder" in result.output.lower()


@pytest.mark.smoke
def test_placeholder_does_not_execute() -> None:
    result = runner.invoke(app, ["optimize"])

    assert result.exit_code == 0
    assert "not implemented in this milestone" in result.output


@pytest.mark.smoke
@pytest.mark.parametrize(
    "command",
    (
        "inspect",
        "analyze",
        "benchmark",
        "optimize",
        "quality",
        "status",
        "report",
        "capsule",
        "export",
        "agent",
        "diagnostics",
        "cleanup",
    ),
)
def test_every_subcommand_help_is_safe(command: str) -> None:
    result = runner.invoke(app, [command, "--help"])

    assert result.exit_code == 0
    assert "placeholder" in result.output.lower()

"""Repository-level security invariants for the foundation."""

from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]


@pytest.mark.security
def test_no_generic_remote_shell_interface_exists() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for root in (ROOT / "agent", ROOT / "packages")
        for path in root.rglob("*.py")
    )

    assert "execute_shell" not in source


@pytest.mark.security
def test_sensitive_artifact_paths_are_ignored() -> None:
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

    for required in (
        "*.safetensors",
        "*.gguf",
        "*.cubin",
        "customer-data/",
        "diagnostic-bundles/",
        "execution-capsules/",
        "deployment-secrets/",
    ):
        assert required in ignore

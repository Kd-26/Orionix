"""Tests for the offline repository-documentation validator."""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]
CHECKER = ROOT / "scripts" / "check_docs.py"


def _run_checker(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(root)],
        check=False,
        capture_output=True,
        text=True,
    )


@pytest.mark.unit
def test_documentation_check_accepts_existing_file_and_heading_links(tmp_path: Path) -> None:
    guide = tmp_path / "guide.md"
    guide.write_text("# Guide\n\n## Setup steps\n", encoding="utf-8")
    (tmp_path / "README.md").write_text(
        "# Project\n\nRead the [setup](guide.md#setup-steps).\n", encoding="utf-8"
    )

    result = _run_checker(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.unit
def test_documentation_check_rejects_missing_files_and_headings(tmp_path: Path) -> None:
    guide = tmp_path / "guide.md"
    guide.write_text("# Guide\n\n## Existing section\n", encoding="utf-8")
    (tmp_path / "README.md").write_text(
        "# Project\n\n[missing](missing.md) and [bad heading](guide.md#absent).\n",
        encoding="utf-8",
    )

    result = _run_checker(tmp_path)

    assert result.returncode == 1
    assert "missing link target" in result.stdout
    assert "missing heading anchor" in result.stdout

#!/usr/bin/env python3
"""Verify every workspace distribution built a typed Python wheel."""

from __future__ import annotations

import argparse
import tomllib
import zipfile
from pathlib import Path

EXCLUDED_PARTS = {".venv", "build", "dist"}


def _workspace_manifests(root: Path) -> list[Path]:
    return sorted(
        manifest
        for manifest in root.rglob("pyproject.toml")
        if manifest != root / "pyproject.toml"
        and not any(part in EXCLUDED_PARTS for part in manifest.relative_to(root).parts)
    )


def validate_build_artifacts(root: Path) -> list[str]:
    """Return errors for missing wheels or typed-package markers."""

    root = root.resolve()
    dist = root / "dist"
    errors: list[str] = []
    expected_wheels: set[Path] = set()

    for manifest in _workspace_manifests(root):
        parsed = tomllib.loads(manifest.read_text(encoding="utf-8"))
        project = parsed.get("project")
        if not isinstance(project, dict):
            errors.append(f"{manifest.relative_to(root)}: missing [project] table")
            continue

        name = project.get("name")
        version = project.get("version")
        if not isinstance(name, str) or not isinstance(version, str):
            errors.append(f"{manifest.relative_to(root)}: project name/version must be strings")
            continue

        normalized_name = name.replace("-", "_")
        matches = sorted(dist.glob(f"{normalized_name}-{version}-*.whl"))
        if len(matches) != 1:
            errors.append(f"{name}: expected one wheel for version {version}, found {len(matches)}")
            continue

        wheel = matches[0]
        expected_wheels.add(wheel)
        marker = f"{normalized_name}/py.typed"
        with zipfile.ZipFile(wheel) as archive:
            if marker not in archive.namelist():
                errors.append(f"{wheel.name}: missing {marker}")

    unexpected = sorted(set(dist.glob("*.whl")) - expected_wheels)
    for wheel in unexpected:
        errors.append(f"unexpected wheel in dist: {wheel.name}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate_build_artifacts(args.root)
    if errors:
        print("Build-artifact validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    count = len(_workspace_manifests(args.root.resolve()))
    print(f"Build-artifact validation passed for {count} typed wheels.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

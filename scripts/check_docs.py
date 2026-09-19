#!/usr/bin/env python3
"""Validate repository Markdown and its internal links without network access."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote

LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\((?P<destination><[^>]+>|[^)\s]+)")
HEADING_PATTERN = re.compile(r"^(?P<level>#{1,6})\s+(?P<title>.+?)\s*#*\s*$", re.MULTILINE)
EXCLUDED_PARTS = {".git", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".venv", "build", "dist"}


def _slug(title: str) -> str:
    """Return the GitHub-style anchor used by the repository's plain headings."""

    without_markup = re.sub(r"[`*_~]", "", title.lower())
    without_punctuation = re.sub(r"[^\w\- ]", "", without_markup)
    return re.sub(r"\s+", "-", without_punctuation.strip())


def _heading_anchors(markdown: str) -> set[str]:
    anchors: set[str] = set()
    occurrences: dict[str, int] = {}
    for match in HEADING_PATTERN.finditer(markdown):
        base = _slug(match.group("title"))
        count = occurrences.get(base, 0)
        occurrences[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def _markdown_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.md")
        if not any(part in EXCLUDED_PARTS for part in path.relative_to(root).parts)
    )


def validate_repository(root: Path) -> list[str]:
    """Return human-readable validation errors for Markdown under ``root``."""

    root = root.resolve()
    errors: list[str] = []
    document_cache: dict[Path, str] = {}
    anchor_cache: dict[Path, set[str]] = {}

    for source in _markdown_files(root):
        relative_source = source.relative_to(root)
        try:
            markdown = source.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{relative_source}: file is not valid UTF-8")
            continue

        document_cache[source] = markdown
        for match in LINK_PATTERN.finditer(markdown):
            destination = match.group("destination").strip("<>")
            line = markdown.count("\n", 0, match.start()) + 1
            if destination.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
                continue

            path_text, separator, anchor = destination.partition("#")
            target = source if not path_text else source.parent / unquote(path_text)
            target = target.resolve()

            try:
                target.relative_to(root)
            except ValueError:
                errors.append(
                    f"{relative_source}:{line}: local link leaves repository: {destination}"
                )
                continue

            if not target.exists():
                errors.append(f"{relative_source}:{line}: missing link target: {destination}")
                continue

            if separator and anchor and target.suffix.lower() == ".md":
                if target not in document_cache:
                    try:
                        document_cache[target] = target.read_text(encoding="utf-8")
                    except UnicodeDecodeError:
                        errors.append(
                            f"{relative_source}:{line}: linked file is not valid UTF-8: "
                            f"{destination}"
                        )
                        continue
                anchors = anchor_cache.setdefault(target, _heading_anchors(document_cache[target]))
                if unquote(anchor).lower() not in anchors:
                    errors.append(
                        f"{relative_source}:{line}: missing heading anchor: {destination}"
                    )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate_repository(args.root)
    if errors:
        print("Documentation validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    count = len(_markdown_files(args.root.resolve()))
    print(f"Documentation validation passed for {count} Markdown files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

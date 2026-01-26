#!/usr/bin/env python3
"""
Minimal Markdown/YAML linter.

Rules:
- No tabs
- No trailing whitespace
- Files must end with a newline
- YAML must parse via PyYAML (safe_load)
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

EXCLUDE_PREFIXES = (
    "legacy/",
    "runs/",
    "node_modules/",
    ".venv/",
)


def list_tracked_files() -> list[Path]:
    output = subprocess.check_output(["git", "ls-files"], text=True)
    return [Path(line.strip()) for line in output.splitlines() if line.strip()]


def is_excluded(path: Path) -> bool:
    path_str = path.as_posix()
    return path_str.startswith(EXCLUDE_PREFIXES)


def check_text_rules(path: Path, content: str) -> list[str]:
    errors: list[str] = []
    for idx, line in enumerate(content.splitlines(), start=1):
        if "\t" in line:
            errors.append(f"{path}:{idx}: contains tab character")
        if line.rstrip("\n") != line.rstrip():
            errors.append(f"{path}:{idx}: trailing whitespace")
    if content and not content.endswith("\n"):
        errors.append(f"{path}: missing trailing newline at EOF")
    return errors


def lint_yaml(path: Path, content: str) -> list[str]:
    errors = check_text_rules(path, content)
    try:
        yaml.safe_load(content)
    except Exception as exc:  # noqa: BLE001 - explicit for linting output
        errors.append(f"{path}: YAML parse error: {exc}")
    return errors


def lint_markdown(path: Path, content: str) -> list[str]:
    return check_text_rules(path, content)


def main() -> int:
    errors: list[str] = []

    for path in list_tracked_files():
        if is_excluded(path) or not path.exists() or path.is_dir():
            continue
        suffix = path.suffix.lower()
        if suffix not in {".md", ".yaml", ".yml"}:
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        if suffix in {".yaml", ".yml"}:
            errors.extend(lint_yaml(path, content))
        else:
            errors.extend(lint_markdown(path, content))

    if errors:
        for error in errors:
            print(error)
        print(f"\nFound {len(errors)} lint error(s).")
        return 1

    print("✓ Markdown/YAML lint passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

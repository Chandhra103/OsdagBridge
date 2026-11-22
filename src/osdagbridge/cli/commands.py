"""Command implementations for the currently supported CLI subset."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from osdagbridge.core.utils.validation import project_file_errors


PROJECT_TEMPLATE = {
    "project": {"name": "New bridge project", "bridge_type": "plate_girder", "span_m": 20.0}
}


def read_project(path: str | Path) -> Any:
    """Read a UTF-8 JSON project file."""
    with Path(path).open("r", encoding="utf-8") as stream:
        return json.load(stream)


def init_cmd(path: str | Path, *, force: bool = False) -> int:
    target = Path(path)
    if target.exists() and not force:
        print(f"Error: {target} already exists (use --force to replace it).")
        return 2
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(PROJECT_TEMPLATE, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        print(f"Error: could not write {target}: {exc}")
        return 2
    print(f"Created starter JSON project: {target}")
    print("Edit project.name and project.span_m; this file is not a complete design input set.")
    return 0


def validate_cmd(path: str | Path) -> int:
    try:
        data = read_project(path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Error: could not read JSON project {path}: {exc}")
        return 2
    errors = project_file_errors(data)
    if errors:
        for error in errors:
            print(f"Invalid project: {error}")
        return 1
    project = data["project"]
    print(f"Project file is structurally valid: {project['name']} ({project['span_m']} m)")
    print("Note: this does not validate engineering inputs or design adequacy.")
    return 0


def inspect_cmd(path: str | Path) -> int:
    try:
        data = read_project(path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Error: could not read JSON project {path}: {exc}")
        return 2
    errors = project_file_errors(data)
    if errors:
        for error in errors:
            print(f"Invalid project: {error}")
        return 1
    project = data["project"]
    print(f"Name: {project['name']}\nType: {project.get('bridge_type', 'unspecified')}\nSpan: {project['span_m']} m")
    return 0


def analyze_cmd(path: str | Path) -> int:
    """Refuse analysis rather than returning fabricated engineering results."""
    print(f"Analysis was not run for {path}.")
    print("The CLI project envelope is not wired to the plate-girder engineering pipeline.")
    return 2

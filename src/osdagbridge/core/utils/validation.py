"""Lightweight project-file validation (not structural-engineering validation)."""
from __future__ import annotations

import math
from typing import Any


def project_file_errors(data: Any) -> list[str]:
    """Return schema errors for the small JSON project envelope used by the CLI.

    This deliberately checks file shape and a positive span only. It does not
    validate the full set of design inputs, codes, or engineering adequacy.
    """
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["The JSON document must contain an object at its root."]

    project = data.get("project")
    if not isinstance(project, dict):
        return ["Missing required object: project."]

    name = project.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("project.name must be a non-empty string.")

    span = project.get("span_m")
    if isinstance(span, bool) or not isinstance(span, (int, float)):
        errors.append("project.span_m must be a positive finite number in metres.")
    elif not math.isfinite(span) or span <= 0:
        errors.append("project.span_m must be a positive finite number in metres.")
    return errors


def validate_project(data: Any) -> bool:
    """Return whether *data* meets the lightweight CLI project-file schema.

    This is a compatibility-friendly boolean wrapper; use
    :func:`project_file_errors` to retrieve diagnostics.
    """
    return not project_file_errors(data)

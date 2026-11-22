"""Result access helpers shared by longitudinal and transverse plot views.

Values are read only from analysis-result dictionaries produced by
``results_data.restructure_data``; this module never estimates missing results.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence

FORCE_COMPONENTS = {
    # These keys are the existing plot-generator keys; the OutputDock labels
    # them Fx/Vy/Vz/Tx/My/Mz. The result arrays store endpoint components.
    "Fx": ("Vx_i", "Vx_j"), "Fy": ("Vy_i", "Vy_j"),
    "Fz": ("Vz_i", "Vz_j"), "Mx": ("Mx_i", "Mx_j"),
    "My": ("My_i", "My_j"), "Mz": ("Mz_i", "Mz_j"),
}
DISPLACEMENT_COMPONENTS = {"Dx": "x", "Dy": "y", "Dz": "z"}


def transverse_member_groups(data: Mapping) -> dict[str, list[str]]:
    """Return separately selectable transverse groups without altering tag IDs."""
    groups = {"End Diaphragms": [], "Intermediate Cross Bracings": []}
    for record in data.get("end_diaphragms", []) or []:
        groups["End Diaphragms"].extend(str(tag) for tag in record.get("members", []))
    for record in data.get("crossbracings", []) or []:
        groups["Intermediate Cross Bracings"].extend(
            str(tag) for tag in record.get("members", [])
        )
    # Explicit group metadata from callers takes precedence/adds tags, not guesses.
    raw = data.get("transverse_groups", {}) or {}
    for label, aliases in {
        "End Diaphragms": ("end_diaphragm", "end_diaphragms"),
        "Intermediate Cross Bracings": ("intermediate_cross_bracing", "crossbracing", "crossbracings"),
    }.items():
        for alias in aliases:
            groups[label].extend(str(tag) for tag in raw.get(alias, []) or [])
    for label in groups:
        groups[label] = list(dict.fromkeys(groups[label]))
    return groups


def extract_element_component(data: Mapping, loadcase: str, element_tags: Sequence,
                              component: str) -> list[tuple[int, float, float]]:
    """Extract actual endpoint force values for the requested case and tags.

    The returned rows are (element tag, i-end value, j-end value). Missing,
    nonnumeric, or partial result entries are omitted rather than fabricated.
    """
    pair = FORCE_COMPONENTS.get(component)
    if pair is None:
        raise ValueError(f"Unsupported force component: {component}")
    table = (data.get("forces") or {}).get(str(loadcase), {})
    rows = []
    for tag in element_tags:
        entry = table.get(str(tag))
        if not isinstance(entry, Mapping) or any(k not in entry for k in pair):
            continue
        try:
            rows.append((int(tag), float(entry[pair[0]]), float(entry[pair[1]])))
        except (TypeError, ValueError):
            continue
    return rows


def extract_node_component(data: Mapping, loadcase: str, node_tags: Sequence,
                           component: str) -> list[tuple[int, float]]:
    """Extract actual nodal displacement values for a component."""
    key = DISPLACEMENT_COMPONENTS.get(component)
    if key is None:
        raise ValueError(f"Unsupported displacement component: {component}")
    table = (data.get("displacements") or {}).get(str(loadcase), {})
    rows = []
    for tag in node_tags:
        entry = table.get(str(tag))
        if not isinstance(entry, Mapping) or key not in entry:
            continue
        try:
            rows.append((int(tag), float(entry[key])))
        except (TypeError, ValueError):
            continue
    return rows


def get_member_result(data: Mapping, loadcase: str, element_tag: int,
                      component: str) -> tuple[float, float] | None:
    """Fetch endpoint values for one force result, returning None if unavailable."""
    rows = extract_element_component(data, loadcase, [element_tag], component)
    return (rows[0][1], rows[0][2]) if rows else None

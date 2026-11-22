"""Policy and input parsing for interactive 2D CAD dimension edits."""
from __future__ import annotations

import math
from dataclasses import dataclass
from osdagbridge.core.utils.common import (
    KEY_CARRIAGEWAY_WIDTH, KEY_SPAN, KEY_TS_DECK_THICKNESS,
    KEY_TS_GIRDER_SPACING,
)

@dataclass(frozen=True)
class DimensionParameter:
    label: str
    cad_key: str
    input_key: str
    display_to_cad: float
    cad_to_input: float
    input_unit: str
    editable: bool = True

EDITABLE_DIMENSIONS = {
    "Carriageway Width": DimensionParameter("Carriageway Width", "carriageway_width", KEY_CARRIAGEWAY_WIDTH, 1000.0, .001, "m"),
    "Girder Spacing": DimensionParameter("Girder Spacing", "girder_spacing", KEY_TS_GIRDER_SPACING, 1000.0, .001, "m"),
    "Deck Thickness": DimensionParameter("Deck Thickness", "deck_thickness", KEY_TS_DECK_THICKNESS, 1.0, 1.0, "mm"),
    "Span Length": DimensionParameter("Span Length", "span_length", KEY_SPAN, 1000.0, .001, "m"),
}
READ_ONLY_DIMENSIONS = frozenset({"Overhang", "Overall Bridge Width", "Bracing Spacing"})


def parse_dimension_value(text: str) -> float:
    """Parse a finite positive dimension; reject blanks, NaN, infinity, and zero."""
    try:
        value = float(str(text).strip())
    except (TypeError, ValueError) as exc:
        raise ValueError("Enter a numerical dimension.") from exc
    if not math.isfinite(value) or value <= 0:
        raise ValueError("Enter a positive finite dimension.")
    return value


def apply_dimension_edit(input_values: dict, label: str, text: str) -> tuple[dict, float]:
    """Return a validated copy with the parameter converted to its model unit.

    Input values remain untouched when parsing fails or the label is read-only.
    ``value`` in the tuple is in the CAD unit (mm), with input dictionaries
    storing span, carriageway width, and girder spacing in metres.
    """
    if label in READ_ONLY_DIMENSIONS:
        raise ValueError(f"{label} is a derived, read-only dimension.")
    if label not in EDITABLE_DIMENSIONS:
        raise ValueError(f"Unknown editable dimension: {label}")
    value = parse_dimension_value(text)
    parameter = EDITABLE_DIMENSIONS[label]
    updated = dict(input_values)
    cad_value = value * parameter.display_to_cad
    updated[parameter.input_key] = cad_value * parameter.cad_to_input
    return updated, cad_value

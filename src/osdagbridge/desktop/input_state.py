"""Pure helpers for custom-input validation and dialog change tracking."""
from __future__ import annotations


def custom_value_error(parameter_name: str, value, *, selected_custom: bool,
                       enabled: bool = True, applicable: bool = True) -> str | None:
    """Return the prescribed error for an applicable, enabled blank Custom value."""
    if not selected_custom or not enabled or not applicable:
        return None
    if value is not None and str(value).strip():
        return None
    return f"Error: The custom value for '{parameter_name}' cannot be empty."


def values_differ(original, current) -> bool:
    """Compare input state without treating a reloaded/programmatic identical value as dirty."""
    return original != current

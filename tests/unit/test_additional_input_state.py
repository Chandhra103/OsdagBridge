"""Custom-value validator tests independent of Qt; widget eligibility is passed explicitly."""
import pytest
from osdagbridge.desktop.input_state import custom_value_error, values_differ

@pytest.mark.parametrize('value', [None, '', '   ', '\t\n'])
def test_empty_custom_value_returns_exact_required_error(value):
    assert custom_value_error('Wind Load', value, selected_custom=True) == (
        "Error: The custom value for 'Wind Load' cannot be empty.")

@pytest.mark.parametrize('value', ['0', 0, ' 12.5 '])
def test_valid_custom_value_is_accepted(value):
    assert custom_value_error('Wind Load', value, selected_custom=True) is None

@pytest.mark.parametrize('flags', [
    {'selected_custom': False}, {'selected_custom': True, 'enabled': False},
    {'selected_custom': True, 'applicable': False},
])
def test_inactive_custom_controls_are_not_rejected(flags):
    assert custom_value_error('Wind Load', '', **flags) is None

def test_modified_state_comparison_tracks_only_actual_value_changes():
    assert values_differ({'x': 1}, {'x': 2})
    assert not values_differ({'x': 1}, {'x': 1})

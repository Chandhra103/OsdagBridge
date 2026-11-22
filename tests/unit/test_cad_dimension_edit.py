"""Pure parameter-policy tests; no GUI or engineering solver is mocked."""
import pytest
from osdagbridge.desktop.cad_dimension_edit import (
    EDITABLE_DIMENSIONS, READ_ONLY_DIMENSIONS, apply_dimension_edit,
    parse_dimension_value,
)
from osdagbridge.core.utils.common import KEY_CARRIAGEWAY_WIDTH, KEY_SPAN, KEY_TS_DECK_THICKNESS, KEY_TS_GIRDER_SPACING

@pytest.mark.parametrize('label', ['Carriageway Width','Girder Spacing','Deck Thickness','Span Length'])
def test_required_editable_labels_are_classified(label):
    assert EDITABLE_DIMENSIONS[label].editable

@pytest.mark.parametrize('label', ['Overhang','Overall Bridge Width','Bracing Spacing'])
def test_derived_labels_are_read_only(label):
    assert label in READ_ONLY_DIMENSIONS
    with pytest.raises(ValueError):
        apply_dimension_edit({}, label, '2')

@pytest.mark.parametrize('text', ['', '   ', 'x', '0', '-1', 'nan', 'inf'])
def test_invalid_dimensions_are_rejected(text):
    with pytest.raises(ValueError):
        parse_dimension_value(text)

@pytest.mark.parametrize('label,text,key,expected', [
    ('Carriageway Width','10.5',KEY_CARRIAGEWAY_WIDTH,10.5),
    ('Girder Spacing','2.75',KEY_TS_GIRDER_SPACING,2.75),
    ('Deck Thickness','220',KEY_TS_DECK_THICKNESS,220.0),
    ('Span Length','35',KEY_SPAN,35.0),
])
def test_edit_converts_display_units_to_model_units_without_mutating_source(label,text,key,expected):
    original={key: 1}
    updated, cad_value=apply_dimension_edit(original,label,text)
    assert updated[key] == pytest.approx(expected)
    assert original[key] == 1
    assert cad_value > 0

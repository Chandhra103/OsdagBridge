import pytest

pytest.importorskip("openseespy.opensees", reason="OpenSeesPy is required by the analysis module")

from osdagbridge.core.bridge_types.plate_girder.analyser import BridgeGrillageModel
from osdagbridge.core.bridge_types.plate_girder.dto import DeckLayoutProperties, GrillageGeometry


def test_set_geometry_derives_bridge_width_from_deck_layout(capsys):
    model = BridgeGrillageModel()
    model.set_geometry(
        GrillageGeometry(
            L=24.0,
            n_l=4,
            n_t=5,
            edge_dist=0.5,
            ext_to_int_dist=2.5,
            angle=0.0,
        ),
        DeckLayoutProperties(
            carriageway_width=7.5,
            crash_barrier_width=0.4,
            footpath_width=1.2,
            railing_width=0.1,
            median_width=0.0,
            n_footpaths=2,
        ),
    )

    assert model.L == 24.0
    assert model.n_l == 4
    assert model.bridge_geometry.span == 24.0
    assert model.bridge_geometry.width == pytest.approx(10.9)
    assert model.layout.total_width == pytest.approx(model.bridge_geometry.width)
    capsys.readouterr()  # suppress the method's current diagnostic print

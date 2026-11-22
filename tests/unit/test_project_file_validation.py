import pytest

from osdagbridge.core.bridge_types.plate_girder.bridge_geometry import BridgeGeometry
from osdagbridge.core.bridge_types.plate_girder.load_placement import FootpathLoad
from osdagbridge.core.utils.validation import project_file_errors, validate_project


@pytest.mark.parametrize(
    "data",
    [
        {"project": {"name": "Bridge A", "span_m": 12}},
        {"project": {"name": "Bridge B", "span_m": 0.25}},
    ],
)
def test_valid_project_envelope(data):
    assert validate_project(data)
    assert project_file_errors(data) == []


@pytest.mark.parametrize(
    "data",
    [None,
        [],
        {},
        {"project": {"name": " ", "span_m": 2}},
        {"project": {"name": "Bridge", "span_m": 0}},
        {"project": {"name": "Bridge", "span_m": float("inf")}},
        {"project": {"name": "Bridge", "span_m": True}},
    ],
)
def test_invalid_project_envelope(data):
    assert not validate_project(data)
    assert project_file_errors(data)


def test_footpath_polygon_keeps_configured_start_offset():
    geometry = FootpathLoad(BridgeGeometry(span=30.0, width=12.0), start_offset=1.5, width=2.0).to_global()

    assert (geometry.p1.x, geometry.p1.z) == (0.0, 1.5)
    assert (geometry.p2.x, geometry.p2.z) == (30.0, 1.5)
    assert (geometry.p3.x, geometry.p3.z) == (30.0, 3.5)
    assert (geometry.p4.x, geometry.p4.z) == (0.0, 3.5)


def test_unimplemented_native_solver_raises_instead_of_claiming_success():
    from osdagbridge.core.solvers.native_solver import run_native_analysis

    with pytest.raises(NotImplementedError, match="no analysis was run"):
        run_native_analysis(model={})

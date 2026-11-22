"""Unit tests for result access. The dict below is synthetic test data only."""
import pytest
from osdagbridge.core.bridge_types.plate_girder.transverse_results import (
    extract_element_component, extract_node_component, get_member_result,
    transverse_member_groups,
)

@pytest.fixture
def synthetic_result_fixture():
    # Explicit synthetic values isolate key routing; these are not engineering results.
    return {
        "forces": {"LC-test": {"40": {"Vx_i": 11, "Vx_j": 12,
            "Vy_i": 21, "Vy_j": 22, "Vz_i": 31, "Vz_j": 32,
            "Mx_i": 41, "Mx_j": 42, "My_i": 51, "My_j": 52,
            "Mz_i": 61, "Mz_j": 62}}},
        "displacements": {"LC-test": {"7": {"x": 0.1, "y": 0.2, "z": 0.3}}},
        "crossbracings": [{"members": ["40"]}],
        "end_diaphragms": [{"members": ["41"]}],
    }

@pytest.mark.parametrize("component,expected", [
    ("Fx", (11., 12.)), ("Fy", (21., 22.)), ("Fz", (31., 32.)),
    ("Mx", (41., 42.)), ("My", (51., 52.)), ("Mz", (61., 62.)),
])
def test_force_component_endpoint_mapping(synthetic_result_fixture, component, expected):
    assert get_member_result(synthetic_result_fixture, "LC-test", 40, component) == expected

@pytest.mark.parametrize("component,expected", [("Dx", .1), ("Dy", .2), ("Dz", .3)])
def test_displacement_component_mapping(synthetic_result_fixture, component, expected):
    assert extract_node_component(synthetic_result_fixture, "LC-test", [7], component) == [(7, expected)]

def test_missing_loadcase_or_result_returns_empty(synthetic_result_fixture):
    assert extract_element_component(synthetic_result_fixture, "missing", [40], "Fy") == []
    assert get_member_result(synthetic_result_fixture, "LC-test", 999, "Fy") is None

def test_empty_result_dictionaries_return_no_engineering_values():
    assert extract_element_component({}, "LC", [1], "Fx") == []
    assert extract_node_component({}, "LC", [1], "Dx") == []

def test_groups_preserve_transverse_tag_categories(synthetic_result_fixture):
    groups = transverse_member_groups(synthetic_result_fixture)
    assert groups["Intermediate Cross Bracings"] == ["40"]
    assert groups["End Diaphragms"] == ["41"]

def test_invalid_component_is_reported():
    with pytest.raises(ValueError):
        extract_element_component({}, "LC", [1], "Dx")

def test_ospgrillage_start_and_end_edge_groups_route_to_end_diaphragms():
    # Synthetic topology only: the group names mirror analyser.create_model().
    from osdagbridge.core.bridge_types.plate_girder.results_data_post_processing import post_process

    processed = post_process({
        "nodes": {"1": [0, 0, 0], "2": [0, 0, 1], "3": [1, 0, 0],
                  "4": [1, 0, 1], "5": [2, 0, 0], "6": [2, 0, 1]},
        "members": {"31": [1, 2], "30": [2, 4], "32": [4, 6]},
        "groups": {"start_edge": ["31"], "transverse_slab": ["30"],
                   "end_edge": ["32"]},
        "loadcases": [], "forces": {}, "displacements": {},
    })
    assert processed["transverse_groups"]["end_diaphragm"] == ["31", "32"]

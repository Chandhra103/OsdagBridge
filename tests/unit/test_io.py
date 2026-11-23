import json

import pytest

from osdagbridge.cli.commands import read_project


def test_read_project_loads_json_object(tmp_path):
    path = tmp_path / "project.json"
    expected = {"project": {"name": "Bridge 1", "span_m": 18.5}}
    path.write_text(json.dumps(expected), encoding="utf-8")

    assert read_project(path) == expected


def test_read_project_reports_malformed_json(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text('{"project":', encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        read_project(path)

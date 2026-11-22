import json

from osdagbridge.cli.__main__ import main


def test_init_validate_and_inspect_project(tmp_path, capsys):
    path = tmp_path / "bridge.json"

    assert main(["init", str(path)]) == 0
    created = json.loads(path.read_text(encoding="utf-8"))
    assert created["project"]["span_m"] == 20.0

    assert main(["validate", str(path)]) == 0
    assert "does not validate engineering inputs" in capsys.readouterr().out

    assert main(["inspect", str(path)]) == 0
    output = capsys.readouterr().out
    assert "New bridge project" in output
    assert "20.0 m" in output


def test_validate_rejects_invalid_project(tmp_path, capsys):
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps({"project": {"name": "", "span_m": -3}}), encoding="utf-8")

    assert main(["validate", str(path)]) == 1
    output = capsys.readouterr().out
    assert "project.name" in output
    assert "positive finite number" in output


def test_analyze_does_not_claim_success(tmp_path, capsys):
    path = tmp_path / "bridge.json"

    assert main(["analyze", str(path)]) == 2
    output = capsys.readouterr().out
    assert "Analysis was not run" in output
    assert "not wired" in output


def test_init_does_not_overwrite_without_force(tmp_path, capsys):
    path = tmp_path / "existing.json"
    path.write_text("{}", encoding="utf-8")

    assert main(["init", str(path)]) == 2
    assert path.read_text(encoding="utf-8") == "{}"
    assert "already exists" in capsys.readouterr().out

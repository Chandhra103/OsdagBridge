# OsdagBridge

OsdagBridge is an open-source Python project for bridge modelling and analysis, with a substantial plate-girder workflow and a PySide6 desktop application. The repository also contains early web scaffolding and a small project-file CLI; those interfaces are not yet end-to-end engineering applications.

> **Status:** This repository is under active development. The desktop plate-girder workflow is the principal implemented interface. The CLI currently handles a lightweight JSON project envelope only. The Django and React directories are scaffolding, not a usable or deployed web application. No general solver interchangeability is claimed.

## Current capabilities

- Plate-girder input, design/analysis orchestration, reporting and visualization code in `src/osdagbridge/core/bridge_types/plate_girder/` and `src/osdagbridge/desktop/`.
- Task 2 desktop improvements on the [`task2-ui-cad-transverse-plotting` branch](https://github.com/Chandhra103/OsdagBridge/tree/task2-ui-cad-transverse-plotting): inline CAD dimension editing, additional-input state/validation, and transverse member plots.
- CLI commands to create, validate, and inspect a small JSON project-file envelope. This is not the full bridge-design input schema and does not run analysis.
- A read-only starter geometry and lightweight schema test suite. Validation of this small envelope is not engineering validation.

## Requirements and installation

Use Python 3.11 or 3.12. For the desktop application, the repository's Conda environment is recommended because Osdag, Qt, and CAD dependencies may be needed:

```bash
git clone https://github.com/Chandhra103/OsdagBridge.git
cd OsdagBridge
conda env create -f environment.yml
conda activate osdagbridge-env
python -m pip install -e .
```

The package declares `osdagbridge-cli` for CLI project utilities and `osdagbridge` for the desktop entry point. Desktop startup depends on the complete Osdag/Qt/CAD runtime; it is not verified on every platform.

## CLI (limited project-file utilities)

The CLI currently reads JSON, not YAML. Create a starter file, then inspect or validate it:

```bash
osdagbridge-cli --help
osdagbridge-cli init bridge.json
osdagbridge-cli validate bridge.json
osdagbridge-cli inspect bridge.json
```

The starter envelope contains `project.name`, `project.bridge_type`, and `project.span_m`. `validate` checks only JSON shape and a positive finite span; it does not assess design inputs, code compliance, or structural adequacy. `analyze` currently exits nonzero and explicitly reports that analysis is not wired to this CLI. Report generation, solver selection, and export commands are not available through the CLI.

## Desktop

With the project environment installed, launch with:

```bash
python -m osdagbridge.desktop
```

Task 2 behavior and operating notes are described in [`docs/INTERNSHIP_SUBMISSION.md`](docs/INTERNSHIP_SUBMISSION.md). Interactive GUI behavior requires a supported graphical runtime and has not been exhaustively tested in this environment.

## Web status

The repository's Django backend and React frontend are placeholders. There is no complete API, integrated frontend, or deployment configuration. Do not run the old web commands found in earlier documentation as if they started a functional application. No public deployment URL is available.

## Tests

Run from the repository root:

```bash
PYTHONPATH=src python -m pytest -q
```

The CI workflow is `.github/workflows/python-tests.yml`. A passing Python test suite does not verify solver engineering accuracy, interactive GUI behavior, or deployment. See [`docs/TESTING.md`](docs/TESTING.md) for the scope and limitations.

## Development documentation

- [Architecture and capability boundaries](docs/architecture.md)
- [User guide](docs/user_guide.md)
- [Developer guide](docs/developer_guide.md)
- [Test scope and verification](docs/TESTING.md)
- [Master development audit](docs/MASTER_DEVELOPMENT_AUDIT.md)
- [Test report](docs/TEST_REPORT.md)
- [Final acceptance matrix](docs/FINAL_ACCEPTANCE_REPORT.md)
- [Licensing and dependency review](docs/LICENSING_AND_DEPENDENCIES.md)
- [Known limitations](docs/KNOWN_LIMITATIONS.md)
- [Development progress](docs/DEVELOPMENT_PROGRESS.md)
- [Project report](docs/PROJECT_REPORT.md)
- [FOSSEE Task 2 implementation summary](docs/INTERNSHIP_SUBMISSION.md)
- [Known deployment blockers](docs/DEPLOYMENT.md)

## Project layout

- `src/osdagbridge/core/` — shared engineering and geometry modules
- `src/osdagbridge/desktop/` — PySide6 desktop application
- `src/osdagbridge/cli/` — small JSON project-file CLI
- `web/` — incomplete Django/React scaffolding
- `tests/` — unit and integration tests

## Contributing and license

Please run the test suite before proposing changes and distinguish verified behavior from work in progress. **The repository has a license conflict:** `LICENSE` contains GPLv3 text, while `pyproject.toml` advertises an MIT classifier and older project descriptions claim MIT. No license choice has been made here; see [`docs/LICENSING_AND_DEPENDENCIES.md`](docs/LICENSING_AND_DEPENDENCIES.md) and resolve this with the project owner before redistribution.

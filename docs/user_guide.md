# User guide

## Desktop application

Install the project in its recommended Python 3.11/3.12 Conda environment (see `environment.yml`), then run:

```bash
python -m osdagbridge.desktop
```

A full Osdag/Qt/CAD environment may be required. In the typical-section view, the Task 2 workflow supports editing Carriageway Width, Girder Spacing, and Deck Thickness by double-clicking their labels. Span Length can be edited from the top/plan view. Enter or focus loss applies a valid value; Escape cancels. Derived dimensions are read-only. Additional Inputs blocks blank custom values and warns about unsaved changes. After analysis, transverse result views are available when actual results exist; the UI does not synthesize missing results.

These GUI workflows have not been exhaustively exercised in the current headless session. Use only actual analysis outputs and review project assumptions before engineering use.

## CLI project-file utilities

The current CLI handles JSON starter files only:

```bash
osdagbridge-cli init bridge.json
osdagbridge-cli validate bridge.json
osdagbridge-cli inspect bridge.json
```

`init` refuses to overwrite a file unless `--force` is supplied. A starter file resembles:

```json
{
  "project": {
    "name": "New bridge project",
    "bridge_type": "plate_girder",
    "span_m": 20.0
  }
}
```

Validation checks only that the document has a project object, non-empty project name, and positive finite span. It is not engineering validation. CLI analysis, design checks, reports, and YAML loading are not implemented.

## Web application

There is no usable web workflow or hosted application at this time. The Django and React directories are incomplete scaffolds; no deployment URL is available.

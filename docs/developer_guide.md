# Developer guide

## Environment

Use Python 3.11 or 3.12. The repository's `environment.yml` is the intended starting point for the desktop stack:

```bash
conda env create -f environment.yml
conda activate osdagbridge-env
python -m pip install -e .
```

For the existing source-layout test workflow:

```bash
PYTHONPATH=src python -m pytest -q
```

The project's `pyproject.toml` exposes `osdagbridge-cli` for CLI utilities and `osdagbridge` for desktop startup. This session did not build platform installers.

## Safe change practices

Preserve the existing plate-girder core and Task 2 history. Do not treat adapter stubs as working solvers or broaden engineering validation without understanding units, sign conventions, model assumptions, and existing consumers. Add a regression test for behavior changes and verify GUI changes in a real supported Qt environment when possible.

The current CLI project schema is intentionally lightweight and not a bridge design DTO. The web tree is not a working product surface. Avoid claiming either is integrated with the core until actual end-to-end tests demonstrate that integration.

## CI

The repository's GitHub Actions workflow is `.github/workflows/python-tests.yml`. The current checks do not certify structural benchmark accuracy, full desktop interaction, browser behavior, packaging, or deployment.

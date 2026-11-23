# Development Progress

## Current state

- Working branch: `opencode-first-audit`.
- Published web-foundation commit: `7e0090ff498b5fd42d5ad19e612798304489e717` (`Add initial Django and React web workspace`). The code, tests, setup guide, and Vercel guidance are on `origin/opencode-first-audit`.
- GitHub Actions run [45108262874](https://github.com/Chandhra103/OsdagBridge/actions/runs/45108262874) passed: Python suite 61 passed, 3 skipped; dependency-free Node tests 2 passed; backend source compile passed. The skips include analyzer/designer (runner lacks loadable OpenSeesPy native BLAS) and Django API tests (Django/DRF not installed in CI).
- Starting commit: `3db5fc8f7a438335cecb3dd770f3cea287e40f3a`, already published on `complete-osdagbridge-development`.
- The branch retains Task 2 changes. The Task 2 remote is `0b687d6e58507b79e4c1a841cb813821847f2e26`; `dev` was observed at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`. Neither branch has been changed by this work.
- Baseline before this audit: `PYTHONPATH=src python -m pytest -q` — 62 passed.
- `dev` and `task2-ui-cad-transverse-plotting` were preserved; neither was changed by this work.

## Completed before this continuation

The parent development branch contains the limited JSON CLI (`init`, `validate`, `inspect`), explicit refusal to simulate analysis, the correction to `FootpathLoad.to_global`, an explicit unsupported-native-solver exception, tests for those behaviors, updated README/user/developer/architecture docs, an internship summary, and CI that passed 62 tests on the parent commit.

## Fresh findings

The actual web code is at root `web/`, not under `src/osdagbridge/web/`. At the start of this continuation, `web/backend/manage.py` was a scaffold and `web/frontend/src/App.jsx` returned `null`; this continuation now adds an initial Django/React vertical slice, described below. Solver adapters and additional bridge types still include stubs. Three assert-only unit tests were replaced with behavior tests; one default-collected API placeholder remains, and `tests/integration/verification_ddcl_cases.py` is not discovered by pytest's default filename pattern. Licensing and dependency declarations conflict; see the dedicated audit files.

## This continuation

- Re-established baseline on the named work branch: 62 passed.
- Added the requested master feature audit, license/dependency review, final acceptance matrix, test report, known limitations, project report, and this continuation log.
- Replaced the no-op unit tests for analyser setup, DCR classification, and project JSON reading with behavioral tests. Analyzer/designer tests are dependency-guarded because OpenSeesPy is missing in this environment.
- Declared PyYAML, which is imported by desktop YAML project save/load, in `pyproject.toml`, `requirements.txt`, and `environment.yml`. No package installation was performed.
- Updated README license wording to state the actual metadata conflict without selecting a license. No fake engineering or web functionality was introduced.
- Latest local checks: `tests/unit/test_io.py` — 2 passed; full suite — 61 passed, 2 skipped (OpenSeesPy unavailable); compileall, TOML parsing, README documentation-link audit, and `git diff --check` passed. After CI exposed an OpenSeesPy loader exception rather than a missing module, the guards were updated to skip only if the dependency fails to import; the tests still run when it loads successfully.
- Latest remote verification: GitHub Actions run 45104162018 passed on commit `7c380548d7774423d9f0fc105803861d1913a9e7` (61 passed, 2 skipped). The earlier run on `3c0f55e` failed collection because the native library could not load; the guard fix resolved that CI failure without hiding test failures after successful import.
- Current continuation — web foundation: added Django project settings/entry points, SQLite development configuration, initial schema migration, REST session-auth endpoints with CSRF checks, profile persistence, owner-isolated bridge-project CRUD, input-only JSON export, basic finite-positive geometry input validation, and OpenAPI/Swagger routes. Added a responsive React/Vite workspace wired to those APIs for registration/login, profile settings, project create/list/edit/delete, and JSON project-input export. Added Vercel root-directory guidance for the actual `web/frontend` layout. Analysis is explicitly unavailable; no calculations/results are fabricated. Added Django API test cases and a Node test for the actual geometry-serialization helper. A read-only code review caught and the source migration now addresses the fresh-database table-creation gap.
- Current local checks: Python compileall on `web/backend` passed; Node built-in frontend tests — 2 passed; root pytest — 61 passed, 3 skipped. One additional skip is the Django API test module because Django/DRF are not installed. `git diff --check` passed. CI now compiles backend source and runs the dependency-free Node test without installing the web packages. Django API tests, actual migrations, server startup, frontend Vite build, and browser/API integration remain unverified because those packages have not been installed.
- Dependency approval is pending for this exact first-stage set: Django 5.2, Django REST Framework 3.16, django-cors-headers 4.7, drf-spectacular 0.29; React/react-dom 19.2, Vite 7.1, and `@vitejs/plugin-react` 5.0. No packages have been installed. PostgreSQL, solver, charts, and E2E browser packages are excluded from this request.

## Next exact work

1. Await explicit approval before installing the listed web dependencies, then run migrations/API tests, start the API, build the frontend, and verify Vite-to-Django integration.
2. Add authenticated material/section data, loads/combinations, engineering service integration only after validating reusable core services; analysis/results remain unavailable until a tested solver path exists.
3. Resolve with the project owner the GPLv3-versus-MIT metadata conflict before any release/distribution; perform third-party license attribution review.
4. Extend tests and security/configuration work; password reset, PostgreSQL production support, CAD/3D, reports beyond input JSON, and browser end-to-end acceptance remain incomplete.
5. Verify solver workflows against reference cases and supported environments before claiming engineering accuracy. No deployment, installer or release should be claimed before it exists and is verified.

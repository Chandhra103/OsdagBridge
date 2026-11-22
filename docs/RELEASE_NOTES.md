# Development branch notes

## Unreleased — complete-osdagbridge-development

Based on Task 2 commit `0b687d6e58507b79e4c1a841cb813821847f2e26`.

- Replaced the unconditional project validator with explicit lightweight JSON-envelope checks.
- Added CLI `init`, `validate`, `inspect`, and an honest `analyze` response that reports analysis was not run.
- Changed the unimplemented native solver from a success-shaped return to an explicit `NotImplementedError`.
- Fixed the standalone footpath load polygon's second point to preserve its configured lateral offset.
- Replaced README feature and usage claims that described unavailable CLI/web functionality.
- Added architecture, user, developer, testing, deployment, and Task 2 submission documentation.

Post-change verification: `PYTHONPATH=src python -m pytest -q` — 62 passed; `python -m compileall -q src/osdagbridge tests`, `git diff --check`, and CLI help/init/validate smoke checks completed successfully. This is a work-in-progress branch, not a versioned release. It has no release artifacts or deployment URL. Remote push status should be updated from actual execution before any release is prepared.

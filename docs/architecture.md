# Architecture and capability boundaries

## Current structure

`src/osdagbridge/core/` contains shared geometry, bridge components, code utilities, solver-related modules, reporting, and the plate-girder workflow. `PlateGirderBridge` owns the existing end-to-end desktop/core design orchestration. The desktop application in `src/osdagbridge/desktop/` is the primary user-facing interface and consumes this core.

`src/osdagbridge/cli/` provides a separate, deliberately small JSON project-file utility. It currently validates only a starter envelope and is not connected to `PlateGirderBridge`. The Django and React folders under `src/osdagbridge/web/` are scaffolds: the backend entrypoint is not a functioning API and the React app does not implement an interface.

## Solver and engineering status

The repository contains OpenSeesPy and OspGrillage-related modules and an existing analysis/design path. Their presence does not establish support for every model or interchangeable solver behavior. The generic native solver adapter is not a solver and must not be treated as one. Solver correctness and engineering adequacy require benchmark/reference verification beyond the automated tests reported here.

## CLI project envelope

The current CLI accepts JSON with a `project` object containing a non-empty `name` and positive finite `span_m`; `bridge_type` is optional metadata. This preliminary file check is not the full bridge input schema, design validation, or engineering approval. The CLI `analyze` command intentionally returns a nonzero result and says analysis was not run.

## Preserved Task 2 behavior

The existing Task 2 branch remains the source of the CAD dimension editing, additional-input validation/state handling, and transverse plotting changes. This broader development branch is based on its published Task 2 commit and does not rewrite that history.

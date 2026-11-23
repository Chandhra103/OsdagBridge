# Licensing and Dependency Review

**This is a repository inventory, not legal advice. No license selection, compatibility conclusion, or redistribution permission is asserted.**

## Repository license declarations

The root `LICENSE` contains the GNU General Public License version 3 text. In contrast, `pyproject.toml` includes an MIT classifier, and older project descriptions/README revisions claimed MIT. `pyproject.toml` points its license field at the GPLv3-text `LICENSE`, so the classifier/description is inconsistent with that file. This report does not silently resolve the conflict. Obtain the project owner's decision and qualified review; then make all metadata, notices and distribution terms consistent.

The tracked source tree includes `src/ospgrillage/`, but the tracked repository contains no separate license, copying, notice, or third-party attribution file for that code. The manifests also reference Osdag, OpenSeesPy, opsvis, IfcOpenShell, and other packages; their current versions and distribution terms have not been independently reviewed here. Verify each package's license and the provenance/redistribution terms of vendored code before bundling installers or redistributing binaries.

## Dependency manifest comparison

| Dependency/capability | `pyproject.toml` | `requirements.txt` | `environment.yml` | `conda-recipe/meta.yaml` | Finding |
|---|---|---|---|---|---|
| Python | `>=3.11,<3.13` | — | `>=3.11,<3.13` | `>=3.11,<3.13` | broadly aligned |
| SciPy/Fiona/Shapely/Pydantic/xarray | declared | mostly declared | declared | declared | version constraints are not consistently pinned |
| Matplotlib | declared | not listed | declared | `matplotlib-base` | package names differ |
| OpenSeesPy/opsvis | declared | not listed | pip-installed | installed by post-link hook, not recipe run requirements | install path differs |
| PySide6 | absent | declared `>=6.5,<=6.9.3` | expected through Osdag environment | declared | missing from project package runtime metadata |
| NumPy | absent explicitly | declared | transitive/implicit | declared | explicit declaration differs |
| IfcOpenShell/OpenPyXL | absent | declared | absent directly | declared | export-related dependency mismatch |
| PyYAML | declared in this branch | declared in this branch | declared in this branch | declared | declaration added; clean installation remains unverified |
| Django/DRF | absent | absent | absent | absent | backend not packaged or implemented |
| React/Node tooling | no frontend dependencies or scripts in the minimal manifest | — | — | — | frontend is scaffolding |
| Osdag | absent in project metadata | — | Conda `osdag::osdag` | Conda `osdag` | platform-specific setup is not described by `pip install -e .` alone |

The repository also contains `conda-recipe/` post-link scripts that install/uninstall solver packages via pip. Review these lifecycle scripts and dependency ownership before publishing packages. `conda-recipe/meta.yaml` does not state a license field. No clean-room installer build was run.

## Safe follow-up

The package owner should choose the license and confirm third-party provenance first. After that, define `core`, `desktop`, `solver`, and `web` extras or an equivalent tested environment strategy, avoid duplicate incompatible requirements, add license/notice files for vendored components, then verify clean installs in CI. Do not include proprietary/restricted binaries in a public release until redistribution permission is confirmed.

# Known Limitations

- The working implementation is not a complete bridge-engineering platform. Plate-girder core/desktop code is the most substantial area; independent engineering benchmark validation is still required.
- The generic native solver does not exist; its stub now raises rather than returning fabricated success. OpenSeesPy and OspGrillage adapter files are placeholders and are not proven interchangeable backends.
- CLI functions create, validate and inspect a lightweight JSON envelope only. They do not accept the full bridge input schema, run analysis, select a solver, generate reports, or export design results.
- `web/backend/manage.py` is not a functional Django REST API. The React `App.jsx` renders `null`; there is no connected UI, persistence, authentication, migrations, production config, or deployable web workflow.
- Box-girder and truss packages, as well as some substructure/component modules, contain explicit stubs.
- The desktop app depends on the Osdag/Qt/CAD environment. No interactive GUI acceptance run or screenshots were captured in the current task.
- Dependency manifests conflict. PyYAML is now declared across the pip/Conda manifests because source imports it, but no clean install was tested. No large install was attempted.
- The root GPLv3 license text conflicts with an MIT classifier and older MIT claims. No legal decision or third-party license inventory has been completed.
- One default-collected web API test still uses `assert True`; it contributes no meaningful coverage because there is no API implementation. A separate assert-only DDCL file is not discovered by default pytest naming. The analyzer and designer behavior tests are skipped locally because OpenSeesPy is unavailable.
- No web deployment URL, installer, release artifact, or production security/performance evaluation exists.

# OsdagBridge Web (development slice)

This folder contains an early, local-development web application: a Django REST API and a React/Vite client. It currently supports session accounts, profile editing, private project CRUD, basic positive-finite-number geometry input validation, and JSON export of saved project inputs. It does **not** run structural analysis, design checks, or generate engineering reports.

## Requirements

- Python 3.11 or 3.12
- Node.js 20.19+ (22 recommended) and npm
- Dependencies declared in `backend/requirements.txt` and `frontend/package.json`

## Backend setup

From the repository root:

```bash
cd web/backend
python3 -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

For an administrator account, in a second backend terminal with the virtual environment active, run `python manage.py createsuperuser`.

The local SQLite file is `web/backend/db.sqlite3` by default and is ignored by Git. Override its location with `DJANGO_DB_PATH`. `DJANGO_DEBUG` defaults to `true` for local development. Set `DJANGO_SECRET_KEY` to a private random value before any non-debug use. Optional host/origin variables are comma-separated: `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, and `DJANGO_CORS_ALLOWED_ORIGINS`. The Vite development proxy makes local browser/API traffic same-origin; CORS is not a substitute for CSRF protection.

## Frontend setup

In a separate terminal from the repository root:

```bash
cd web/frontend
npm install
npm run dev
```

Open the local URL printed by Vite (normally `http://127.0.0.1:5173`). Vite forwards `/api` and `/health` to the backend at `http://127.0.0.1:8000`. To use another API base URL, define `VITE_API_BASE` in the frontend environment before starting Vite and configure Django CORS/CSRF trusted origins accordingly.

Build the static frontend with `npm run build`; output is written to `web/frontend/dist/`. No production hosting or deployment is configured by this slice.

## Vercel

The repository root is not a Vercel Python function. For a frontend-only Vercel preview, deploy the `opencode-first-audit` branch and set the Vercel project's **Root Directory** to `web/frontend`; use the Vite preset, `npm run build`, and `dist` as the output directory. The earlier `PYTHON_ENTRYPOINT_NOT_FOUND` deployment used the `dev` branch and attempted to detect a Python application at the repository root. That branch does not contain this new frontend implementation.

This setting only builds the static frontend. The current code has no hosted Django API or Vercel service routing, and `VITE_API_BASE` defaults to `/api`; therefore account/project operations will not work on a static Vercel deployment until a compatible Django API is deployed and routed. Do not treat a successful static frontend build as a working full-stack deployment.

## API surface

- `GET /health/` — process health only
- `GET /api/auth/csrf/` — obtain a CSRF token
- `POST /api/auth/register/`, `POST /api/auth/login/`, `POST /api/auth/logout/`
- `GET|PATCH /api/auth/me/` — authenticated profile
- `GET|POST /api/projects/`, `GET|PATCH|PUT|DELETE /api/projects/{id}/`
- `GET /api/projects/{id}/export/` — saved input JSON only
- `POST /api/geometry/validate/` — basic input-shape/range check only
- `GET /api/schema/`, `GET /api/docs/` — OpenAPI schema and Swagger UI

The project API scopes every read/write to the authenticated owner. Session-authenticated unsafe requests require CSRF protection. Account registration uses Django's password hashing and validators.

## Not implemented yet

Password reset, token/OAuth login, material and section catalogs, dedicated load/load-combination APIs, analysis jobs, design checks, results, plots, CAD/3D viewer, engineering reports/PDF/Excel, PostgreSQL/production configuration, frontend automated component/E2E tests, and deployment are not implemented in this slice. Bridge type labels let users organize project records; they do not indicate solver support. Basic geometry validation does not establish bridge safety or design adequacy.

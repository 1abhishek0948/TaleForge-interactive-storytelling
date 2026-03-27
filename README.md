# TaleForge

Full-stack interactive storytelling app:
- Frontend: React + Tailwind (Vite)
- Backend: Django REST Framework + JWT
- Database: PostgreSQL
- Optional: OpenAI-powered dynamic node generation

## Monorepo Layout

```text
backend/   # Django API
frontend/  # React app
```

---

## Local Development

### 1) Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Create local database, then run:

```bash
python manage.py migrate
python manage.py seed_example_stories
python manage.py runserver
```

Backend runs at `http://127.0.0.1:8000`.

Demo login accounts:
- `demo_user / demoxyz12@`
- `moderator_user / moderatorxyz34@`
- `admin_user / adminxyz56@`

The backend can auto-create these users on login if `ENABLE_DEMO_LOGIN_USERS=true`.
`moderator_user` and `admin_user` can edit/manage all stories, nodes, and choices.

### 2) Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend runs at `http://localhost:5173`.

---

## Render Deployment (Single Docker Service + Render Postgres)

This repo is now configured to run **frontend + backend in one Render web service** using:
- root `Dockerfile` (builds React and serves it from Django)
- root `render.yaml` (Render blueprint)

### Deploy steps

1. Push code to GitHub.
2. In Render: `New` -> `Blueprint`.
3. Select this repository.
4. Render creates one web service: `taleforge`.

### Manual (without blueprint)

- Service type: `Web Service`
- Runtime: `Docker`
- Dockerfile path: `./Dockerfile`
- No separate frontend service needed.

### Connect existing Render PostgreSQL

In `taleforge` service env vars, set:

```env
DATABASE_URL=<Render Postgres Internal Database URL>
DB_SSL_REQUIRE=true
```

Use the **Internal Database URL** from your Render Postgres instance (`Connections` tab).

If you only have DB name/password, that is not enough by itself. You also need host, port, and username.

### Required env vars on Render

```env
DEBUG=false
SERVE_FRONTEND_FROM_DJANGO=true
DJANGO_SECRET_KEY=<strong-random-secret>
ALLOWED_HOSTS=.onrender.com
RUN_MIGRATIONS_ON_START=true
RUN_SEED_ON_DEPLOY=false
ENABLE_DEMO_LOGIN_USERS=false
ENABLE_GOOGLE_TRANSLATE_PROXY=true
```

No separate frontend service/env var is needed in single-service mode.
Frontend and API are served from the same domain:
- App: `https://<your-render-service>.onrender.com/`
- API: `https://<your-render-service>.onrender.com/api/`

---

## Useful URLs

- API docs: `https://<your-render-service>.onrender.com/api/docs/`
- OpenAPI schema: `https://<your-render-service>.onrender.com/api/schema/`

---

## Optional OpenAI Setup

Backend env vars:

```env
OPENAI_API_KEY=<your-key>
OPENAI_MODEL=gpt-4.1-mini
```

If missing, AI-choice flows automatically fall back to static next nodes.

## Translation Configuration

Story translation is now proxied via backend (`POST /api/stories/<id>/translate/`) instead of browser-direct third-party calls.

Enable one of these options:

1. OpenAI translation (recommended):

```env
OPENAI_API_KEY=<your-key>
OPENAI_MODEL=gpt-4.1-mini
```

2. Google proxy fallback (less private, but no OpenAI key needed):

```env
ENABLE_GOOGLE_TRANSLATE_PROXY=true
```

Allowed languages are controlled by:

```env
SUPPORTED_TRANSLATION_LANGUAGES=en,hi
```
# TaleForge-interactive-storytelling

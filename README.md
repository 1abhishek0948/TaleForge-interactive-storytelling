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

## Render Deployment (GitHub + Render Postgres)

This repo is now Render-ready with `render.yaml` at project root.

Deploy as **2 services**:
1. `taleforge-backend` (Django web service)
2. `taleforge-frontend` (Vite static site)

### Option A: Blueprint deploy (recommended)

1. Push this repo to GitHub.
2. In Render: `New` -> `Blueprint`.
3. Connect your GitHub repo and deploy.
4. Render reads `render.yaml` and creates both services.

### Option B: Manual service setup

Backend (`backend` root):
- Runtime: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `bash start.sh`

Frontend (`frontend` root):
- Runtime: Static Site
- Build Command: `npm ci && npm run build`
- Publish Directory: `dist`
- Rewrite Rule: `/* -> /index.html`

### Connect existing Render PostgreSQL

In your backend service environment variables, set:

```env
DATABASE_URL=<Render Postgres Internal Database URL>
DB_SSL_REQUIRE=true
```

Use the **Internal Database URL** from your Render Postgres instance (`Connections` tab).

If you only have DB name/password, it is not enough by itself. You also need:
- host
- port
- username

### Required backend env vars on Render

```env
DEBUG=false
DJANGO_SECRET_KEY=<strong-random-secret>
ALLOWED_HOSTS=.onrender.com
RUN_MIGRATIONS_ON_START=true
RUN_SEED_ON_DEPLOY=false
ENABLE_DEMO_LOGIN_USERS=false
ENABLE_GOOGLE_TRANSLATE_PROXY=true
FRONTEND_URL=https://<your-frontend>.onrender.com
CORS_ALLOWED_ORIGINS=https://<your-frontend>.onrender.com
CSRF_TRUSTED_ORIGINS=https://<your-frontend>.onrender.com
```

### Required frontend env var on Render

```env
VITE_API_BASE_URL=https://<your-backend>.onrender.com/api
```

After setting frontend URL/env vars, redeploy backend once so CORS/CSRF values are active.

---

## Useful URLs

- API docs: `https://<your-backend-domain>/api/docs/`
- OpenAPI schema: `https://<your-backend-domain>/api/schema/`

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

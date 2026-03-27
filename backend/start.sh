#!/usr/bin/env bash
set -o errexit

if [ "${RUN_MIGRATIONS_ON_START:-true}" = "true" ]; then
  python manage.py migrate --noinput
fi
python manage.py collectstatic --noinput

# Optional one-time seed on deploy if explicitly enabled.
if [ "${RUN_SEED_ON_DEPLOY:-false}" = "true" ]; then
  python manage.py seed_example_stories
fi

exec gunicorn storytelling.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers ${WEB_CONCURRENCY:-2} \
  --timeout 120

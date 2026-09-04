#!/usr/bin/env bash
set -euo pipefail

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn config.wsgi:application \
    --bind "0.0.0.0:${PORT:-8080}" \
    --workers "${WEB_CONCURRENCY:-1}" \
    --threads "${WEB_THREADS:-2}" \
    --timeout "${GUNICORN_TIMEOUT:-60}"

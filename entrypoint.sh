#!/usr/bin/env bash
# =============================================================================
# entrypoint.sh — Palace Karimi Docker entrypoint
# Waits for PostgreSQL, runs migrations, creates cache table, starts Gunicorn.
# =============================================================================
set -e

# ---------------------------------------------------------------------------
# Wait for PostgreSQL to accept connections
# ---------------------------------------------------------------------------
echo ">>> Waiting for database at ${DB_HOST:-db}:${DB_PORT:-5432}..."
until python -c "
import psycopg2, os, sys
try:
    psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        port=os.environ.get('DB_PORT', '5432'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', ''),
        dbname=os.environ.get('DB_NAME', 'palace_db'),
    )
    sys.exit(0)
except Exception:
    sys.exit(1)
" 2>/dev/null; do
    echo "  ... database not ready, retrying in 2s"
    sleep 2
done
echo ">>> Database is ready."

# ---------------------------------------------------------------------------
# Django setup
# ---------------------------------------------------------------------------
echo ">>> Running migrations..."
python manage.py migrate --noinput

echo ">>> Creating cache table (idempotent)..."
python manage.py createcachetable || true

echo ">>> Collecting static files..."
python manage.py collectstatic --noinput --clear

# ---------------------------------------------------------------------------
# Start application server
# ---------------------------------------------------------------------------
echo ">>> Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -

# Palace Karimi — Frontend Developer Local Environment
# DO NOT commit a real .env file.
# This file is intended for local frontend development only.
# PostgreSQL remains inside Docker, while Django runs locally.

# ==============================================================================
# Django Core
# ==============================================================================

DEBUG=True

SECRET_KEY=django-insecure-local-development-only-change-me

# Local development
ALLOWED_HOSTS=127.0.0.1,localhost

CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000

# ==============================================================================
# PostgreSQL — Docker Database
# ==============================================================================

# IMPORTANT:
# Because Django runs directly on Windows and PostgreSQL runs inside Docker,
# connect through the published Docker host port.

DB_NAME=palace_db
DB_USER=palace_user
DB_PASSWORD=your-local-db-password

DB_HOST=127.0.0.1
DB_PORT=5433

# ==============================================================================
# HTTPS
# ==============================================================================

# Local frontend development does not use HTTPS.
USE_HTTPS=False

# ==============================================================================
# Logging
# ==============================================================================

DJANGO_LOG_LEVEL=INFO

# ==============================================================================
# Optional
# ==============================================================================

# DB_CONTAINER_NAME=palace_postgres

docker compose up -d db

.\venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
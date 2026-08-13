# Palace Karimi — B2B Export Platform

Premium Iranian Saffron and Pistachio export platform built with Django 5.2.

---

## Tech Stack

- **Backend**: Django 5.2, PostgreSQL 16, Gunicorn
- **Frontend**: Bootstrap 4, jQuery, Porto theme (customized)
- **Infrastructure**: Docker, Nginx, python-dotenv
- **Internationalization**: 4 languages (Persian/RTL, English, Arabic, Turkish)

---

## Local Development

### Prerequisites
- Python 3.12+
- A running PostgreSQL instance (see Docker below)

### 1. Start PostgreSQL via Docker

```bash
docker compose up -d db
```

This exposes PostgreSQL on `localhost:5433`.

### 2. Configure `.env`

```bash
cp .env.example .env
# Edit .env — set DB_HOST=127.0.0.1 for local dev
```

Key development settings in `.env`:
```env
DEBUG=True
DB_HOST=127.0.0.1
DB_PORT=5433
```

### 3. Install dependencies

```bash
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 4. Initialize the database

```bash
python manage.py migrate
python manage.py createcachetable   # required for rate limiting
```

### 5. Run the development server

```bash
python manage.py runserver
```

---

## Docker Production Deployment (VPS)

### Prerequisites
- Docker & Docker Compose installed on the VPS
- Domain name pointed to your VPS IP

### Deployment steps

```bash
# 1. Clone the repository
git clone <repo-url> /opt/palace_karimi
cd /opt/palace_karimi

# 2. Configure environment
cp .env.example .env
nano .env  # Fill in real values — DB_HOST=db, DEBUG=False, SECRET_KEY=...

# 3. Build and start containers
docker compose build
docker compose up -d

# The entrypoint.sh automatically runs:
#   - Database migrations
#   - Cache table creation
#   - Static file collection
#   - Gunicorn startup
```

### Stack layout

```
Internet → Nginx (port 80/443) → Gunicorn (port 8000) → Django → PostgreSQL
```

### Verify deployment

```bash
docker compose ps
docker compose logs web
curl http://localhost/fa/
```

---

## Database Backup

```bash
# Create a backup
chmod +x backup.sh
./backup.sh

# Backups are saved to ./backups/palace_db_YYYYMMDD_HHMMSS.sql.gz
# Last 30 backups are kept automatically.

# Restore a backup
gunzip -c backups/palace_db_20260812_120000.sql.gz | \
  docker exec -i palace_postgres psql -U postgres -d palace_db
```

---

## Translations

The project uses Django's i18n system plus `django-rosetta` for in-browser translation editing.

```bash
# Generate/update .po files
python manage.py makemessages -l fa -l en -l ar -l tr

# Compile translations
python manage.py compilemessages

# Access Rosetta in the browser (admin required)
# /rosetta/
```

---

## Management Commands

```bash
# Django system check
python manage.py check

# Run tests
python manage.py test catalog

# Check for pending migrations
python manage.py makemigrations --check --dry-run

# Seed sample data (development only)
python manage.py seed_data
```

---

## Environment Variables Reference

See `.env.example` for the full list of required variables.

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key (required in production) |
| `DEBUG` | `True` for development, `False` for production |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames |
| `DB_HOST` | `127.0.0.1` (local dev) or `db` (Docker) |
| `DB_PASSWORD` | PostgreSQL password |

---

## Notes

- **Rate limiting** uses a database-backed cache table (`rate_limit_cache`). The `entrypoint.sh` creates it automatically in Docker. Run `python manage.py createcachetable` manually in development.
- **HTTPS**: In production, configure SSL certificates and uncomment the HTTPS redirect block in `nginx/default.conf`.
- **Media files**: Uploaded product images are stored in `media/` and served by Nginx at `/media/`.

# Local Development

## Requirements
- Git
- Docker Desktop
- Python 3.12

## Setup

git clone ...
cd ...

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt

Copy-Item .env.example .env

docker compose up -d db

python manage.py migrate

python manage.py collectstatic --noinput

python manage.py runserver

# Restore Existing Database

docker compose up -d db

docker cp .\backups\palace_db.sql palace_postgres:/tmp/palace_db.sql

docker exec palace_postgres psql -U postgres -d palace_db -f /tmp/palace_db.sql
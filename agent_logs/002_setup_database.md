# Task: Setup PostgreSQL Database with Docker

## Files Created

### `docker-compose.yml`

- Created a `docker-compose.yml` file to define a PostgreSQL database service.

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: palace_postgres
    restart: always
    environment:
      - POSTGRES_DB=palace_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=1
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Terminal Commands

The following commands should be executed in a PowerShell terminal:

```pwsh
pip install -r requirements.txt
mkdir locale -ErrorAction SilentlyContinue
docker-compose up -d
Start-Sleep -s 5
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

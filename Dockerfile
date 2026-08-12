# Dockerfile — Palace Karimi B2B Export
# Production-ready multi-stage build with non-root execution
FROM python:3.12-slim AS builder

WORKDIR /build

# Install system build dependencies only (discarded after build)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev gettext \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# ---------------------------------------------------------------------------
# Runtime stage — minimal image, non-root user
# ---------------------------------------------------------------------------
FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for Gunicorn
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

WORKDIR /app

# Copy pre-built Python packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code
COPY --chown=appuser:appuser . /app/

# Ensure entrypoint is executable
RUN chmod +x /app/entrypoint.sh

# Switch to non-root user
USER appuser

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV GUNICORN_CMD_ARGS="--timeout 120 --access-logfile - --error-logfile - --worker-tmp-dir /dev/shm"

# Gunicorn binds inside container; Nginx reverse-proxy handles public port
EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

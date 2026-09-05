# =============================================================================
# Dockerfile — Palace Karimi B2B Export
# Production-ready multi-stage build with non-root execution
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Builder — install Python dependencies
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /build

# Install system build dependencies only (discarded after build)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# ---------------------------------------------------------------------------
# Stage 2: Runtime — minimal image, non-root user
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

# Remove files that should not be in the image
RUN rm -rf /app/venv /app/.git /app/.idea /app/.vscode /app/__pycache__ \
    /app/structures.txt /app/project_summary.md /app/backups

# Pre-collect static files during build for deterministic static serving.
# This bakes the current static assets into the image itself.
RUN python manage.py collectstatic --noinput 2>/dev/null || true

# Ensure entrypoint is executable (fix Windows line endings)
RUN sed -i 's/\r$//' /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Create media directory with correct ownership
RUN mkdir -p /app/media && chown -R appuser:appuser /app/media /app/staticfiles

# Switch to non-root user
USER appuser

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Gunicorn binds inside container; Nginx reverse-proxy handles public port
EXPOSE 8000

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

# Dockerfile
FROM python:3.12-slim

# Set environment variables for better Python performance
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (for PostgreSQL and gettext translations)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install gunicorn

# Copy the entire project
COPY . /app/

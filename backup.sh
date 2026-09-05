#!/usr/bin/env bash
# =============================================================================
# backup.sh — PostgreSQL Backup for Palace Karimi Docker Deployment
#
# Usage:
#   chmod +x backup.sh
#   ./backup.sh                          # uses .env defaults
#   DB_NAME=mydb ./backup.sh             # override env vars
#
# Output:
#   backups/palace_db_YYYYMMDD_HHMMSS.sql.gz
#
# Requires:
#   - Docker Compose or Docker CLI installed
#   - PostgreSQL container must be running
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration (override via env vars or .env file)
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"

if [[ -f "$ENV_FILE" ]]; then
    set -a
    source "$ENV_FILE"
    set +a
fi

CONTAINER_NAME="${DB_CONTAINER_NAME:-palace_postgres}"
DB_NAME="${DB_NAME:-palace_db}"
DB_USER="${DB_USER:-postgres}"
BACKUP_DIR="${BACKUP_DIR:-${SCRIPT_DIR}/backups}"

# ---------------------------------------------------------------------------
# Create backup directory
# ---------------------------------------------------------------------------
mkdir -p "$BACKUP_DIR"

# ---------------------------------------------------------------------------
# Generate filename with timestamp
# ---------------------------------------------------------------------------
TIMESTAMP="$(date '+%Y%m%d_%H%M%S')"
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql.gz"

# ---------------------------------------------------------------------------
# Verify container is running
# ---------------------------------------------------------------------------
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "ERROR: Container '${CONTAINER_NAME}' is not running." >&2
    echo "Available containers:" >&2
    docker ps --format '  - {{.Names}}' >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Run pg_dump inside the container, stream through gzip
# ---------------------------------------------------------------------------
echo ">>> Backing up '${DB_NAME}' from container '${CONTAINER_NAME}'..."
docker exec "$CONTAINER_NAME" \
    pg_dump \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    --no-owner \
    --no-privileges \
    --format=plain \
    2>/dev/null | gzip > "$BACKUP_FILE"

# ---------------------------------------------------------------------------
# Verify backup was created
# ---------------------------------------------------------------------------
if [[ -f "$BACKUP_FILE" && -s "$BACKUP_FILE" ]]; then
    SIZE="$(du -h "$BACKUP_FILE" | cut -f1)"
    echo ">>> Backup successful: ${BACKUP_FILE} (${SIZE})"
else
    echo "ERROR: Backup file is empty or missing." >&2
    rm -f "$BACKUP_FILE"
    exit 1
fi

# ---------------------------------------------------------------------------
# Cleanup: keep only the last 30 backups
# ---------------------------------------------------------------------------
find "$BACKUP_DIR" -name "${DB_NAME}_*.sql.gz" -type f -printf '%T@ %p\n' \
    | sort -n \
    | head -n -30 \
    | awk '{print $2}' \
    | xargs -r rm -f

echo ">>> Old backups cleaned (last 30 retained)."

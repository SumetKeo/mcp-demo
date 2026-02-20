#!/bin/bash
# =============================================================
# mcp-postgres — Database Setup Script
# Usage: bash scripts/setup.sh
# =============================================================

set -e

# Load .env from project root
ENV_FILE="$(dirname "$0")/../.env"
if [ -f "$ENV_FILE" ]; then
  set -o allexport
  source "$ENV_FILE"
  set +o allexport
fi

DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-}
DB_NAME=${DB_NAME:-mcp-demo}

export PGPASSWORD="$DB_PASSWORD"

echo "Creating database '$DB_NAME' if not exists..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres \
  -c "CREATE DATABASE \"$DB_NAME\";" 2>/dev/null || echo "  (already exists, skipping)"

echo "Running init.sql..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
  -f "$(dirname "$0")/init.sql"

echo ""
echo "Done! Tables and mock data created in '$DB_NAME'."

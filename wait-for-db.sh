#!/bin/sh
# wait-for-db.sh
set -e

echo "Waiting for PostgreSQL to be ready..."
until psql "$DATABASE_URL" -c '\q' 2>/dev/null; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "PostgreSQL is up - running migrations"
alembic upgrade head

>&2 echo "Starting API server"
python main.py
#!/bin/sh
# wait-for-db.sh

set -e

# DATABASE_URL format: postgresql://postgres:postgres@postgres/taskmanagement
host=$(echo $DATABASE_URL | cut -d@ -f2 | cut -d/ -f1)
user=$(echo $DATABASE_URL | cut -d/ -f3 | cut -d: -f1)
password=$(echo $DATABASE_URL | cut -d: -f3 | cut -d@ -f1)
db=$(echo $DATABASE_URL | cut -d/ -f4)

echo "Waiting for PostgreSQL to be ready..."
until PGPASSWORD=$password psql -h "$host" -U "$user" -d "$db" -c '\q'; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "PostgreSQL is up - running migrations"
alembic upgrade head

>&2 echo "Starting API server"
exec "$@"

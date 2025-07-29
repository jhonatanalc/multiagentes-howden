#!/bin/bash
set -e

# Wait for PostgreSQL to start
until psql -h postgres -U postgres -d howden_rag -c '\q'; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "PostgreSQL is up - executing schema"

# Execute schema creation
psql -h postgres -U postgres -d howden_rag -f /app/sql/schema.sql

>&2 echo "Schema creation completed"
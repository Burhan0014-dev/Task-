#!/bin/bash
set -e

# Function to create a database
create_database() {
  local database=$1
  echo "Creating database '$database'"
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
      CREATE DATABASE "$database";
EOSQL
}

# List of databases to be created
databases=("Task" "SGC")

for db in "${databases[@]}"; do
  create_database "$db"
done

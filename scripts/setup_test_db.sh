#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! pg_isready -h reservation-postgres -p 5432 -U admin; do
    sleep 1
done

# Create test database
echo "Creating test database..."
PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d reservations_test -c "CREATE DATABASE reservations_test;"

echo "Test database setup complete!" 
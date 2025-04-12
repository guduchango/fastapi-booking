#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! pg_isready -h postgres -p 5432 -U admin; do
    sleep 1
done

# Create test database
echo "Creating test database..."
PGPASSWORD=admin123 psql -h postgres -U admin -d postgres -c "CREATE DATABASE reservations_test;"

echo "Test database setup complete!" 
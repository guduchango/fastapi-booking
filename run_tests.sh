#!/bin/bash

# Install test dependencies
pip install pytest pytest-asyncio httpx

# Create test database
PGPASSWORD=admin psql -h postgres -U admin -d postgres -c "CREATE DATABASE reservations_test;"

# Run tests with PYTHONPATH and TESTING environment variable set
PYTHONPATH=/app TESTING=true pytest tests/ -v

# Clean up test database
PGPASSWORD=admin psql -h postgres -U admin -d postgres -c "DROP DATABASE reservations_test;" 
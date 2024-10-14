#!/bin/sh

# Apply database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the Uvicorn server
echo "Starting Uvicorn server..."
exec uvicorn main:app --host 0.0.0.0 --port 10000

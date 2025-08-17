#!/bin/bash
# start.sh - Railway startup script for dynamic port binding

# Default port if not provided by Railway
PORT=${PORT:-8080}

echo "Starting Gold Trading Calculator on port $PORT"
echo "Flask Environment: $FLASK_ENV"
echo "MT5 Mode: $MT5_MODE"

# Start gunicorn with dynamic port
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --access-logfile - --error-logfile - backend.app:app

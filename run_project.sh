#!/bin/bash

# Find a free port starting from 8081
PORT=8081
while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; do
    echo "Port $PORT is busy, trying next..."
    ((PORT++))
done

echo "Starting Triage System on http://127.0.0.1:$PORT"
echo "Opening browser in 3 seconds..."

# Background open command (Linux/Mac specific)
(sleep 3 && open "http://127.0.0.1:$PORT" || xdg-open "http://127.0.0.1:$PORT") &

python3 manage.py runserver 0.0.0.0:$PORT

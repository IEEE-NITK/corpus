#! /bin/bash

echo "started setup"

echo "checking database connectivity"
python check_database.py
echo "database connected...continuining..."

# Setup database
python manage.py makemigrations
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input

# Start server
gunicorn --bind 0.0.0.0:$DJANGO_BACKEND_PORT --workers 4 corpus.wsgi
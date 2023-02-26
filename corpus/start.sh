#! /bin/bash

echo "started setup"

# Setup database
python manage.py makemigrations
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input

# Start server
gunicorn --bind 0.0.0.0:8000 --workers 4 corpus.wsgi
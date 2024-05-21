#! /bin/sh

echo "started setup"

# Setup database
python manage.py makemigrations
python manage.py migrate --no-input

# Import Config data
python manage.py loaddata config_db.json

# Collect static files
python manage.py collectstatic --no-input

# Start server
gunicorn --bind 0.0.0.0:$DJANGO_BACKEND_PORT --workers 4 corpus.wsgi

#! /bin/bash

export DJANGO_SUPERUSER_PASSWORD=admin

python manage.py migrate --no-input
python manage.py loaddata config_db.json
python manage.py createsuperuser --no-input --email admin@example.com
python manage.py runserver 0.0.0.0:8000

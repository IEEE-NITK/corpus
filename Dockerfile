# IMPORTANT: This Dockerfile will be used by livecycle to
#            generate preview environments for pull requests.

FROM python:3.11.1-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create the working directory
RUN mkdir /corpus
WORKDIR /corpus

# Install dependencies
RUN apt update && apt install -y gcc libpq-dev sqlite3

# Install Python dependencies
COPY corpus/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variables
ENV LIVECYCLE 1
COPY env.example .env

# Copy the application
COPY corpus/ .

# Run the application
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --no-input
RUN python manage.py loaddata config_db.json

EXPOSE 8000
ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "corpus.wsgi" ]

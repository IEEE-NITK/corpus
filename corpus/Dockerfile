FROM python:3.11.1-alpine3.17

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache mariadb-connector-c-dev g++ make
RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt

RUN mv env.example .env

RUN python manage.py makemigrations
RUN python manage.py collectstatic

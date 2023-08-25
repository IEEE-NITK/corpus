FROM python:3.11.1-slim-buster

RUN mkdir /corpus
WORKDIR /corpus

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y gcc libpq-dev

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x ./start.sh
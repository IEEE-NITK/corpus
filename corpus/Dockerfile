FROM python:3.11.1-slim-buster

RUN mkdir /corpus
WORKDIR /corpus

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y gcc libpq-dev curl libmagic1
RUN curl -sL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install -y nodejs

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x ./start.sh
RUN chmod +x ./start_dev.sh

RUN npm i
RUN npm run tailwind-prod

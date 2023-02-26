FROM python:3.11.1-alpine3.17

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache mariadb-connector-c-dev g++ make bash
COPY requirements.txt .
COPY start.sh .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x ./start.sh
CMD [ "/usr/src/app/start.sh" ]

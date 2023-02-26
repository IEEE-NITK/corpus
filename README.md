# IEEE NITK Corpus

A Django based web application to manage all things IEEE NITK.

## Setup Instructions
1. Run the following command to create a copy of the environment file.

```sh
cp django.env.example django.env
cp mariadb.env.example mariadb.env
```

2. Run docker compose

```sh
docker compose up --build
```
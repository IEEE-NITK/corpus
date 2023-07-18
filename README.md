# IEEE NITK Corpus

A Django based web application to manage all things IEEE NITK.

## Setup Instructions

1. Run the following command to create a copy of the environment file.

```sh
cp env.example .env
```

2. Run docker compose

```sh
docker compose up
```

If you have already built the project before, you should rebuild it before getting the services up. Use the following for the same:

```sh
docker compose up --build
```

To stop the containers, just bring the services down.

```sh
docker compose down
```

To remove all the previous data as well, you will have to remove the volumes too. You can do that by appending `-v` to the `down` command.

For more guidance, refer to the [Docker Compose](https://docs.docker.com/compose/) documentation.

## Development Instructions

Versions for all the languages used in the project can be found in the `.tool-versions` file. Support will be provided for all Unix (MacOS, Debian/Ubuntu) based systems. If you choose to develop on Windows, we cannot promise anything xD. We also will not be supporting RHEL-based operating systems.

If you do not have access to a Unix machine, Docker is the recommended way for development.

### Docker Development

This is the preferred way for development. All modern editors allow you to open code in Docker containers remotely. If that is not possible, all code is mounted to Docker containers, so you can make changes that can be checked live.

For development, use the development Docker Compose file.

```shell
docker compose -f dev-docker-compose.yml up --build
```

This Compose file will mount your codebase and add automatic reloading to the frontend code.

If you still choose to go ahead and work on development on individual folders, instructions are given below. However, before development, make sure you source the `.env` file so that all necessary environment variables are picked up.

```shell
set -a
source .env
```

### Frontend
To work on the frontend, make sure you have Nodejs installed on your system. Once you have done that, you can install dependencies and run the server.

```sh
npm install
npm run dev
```

Make sure you properly mark any unnecessary and script generated files in `.gitignore` and `.dockerignore` files.

### Backend
The backend is a Django Rest Framework application. The recommended approach is to create a Python virtual environment, and setup the project.

```sh
python -m venv venv
source venv/bin/activate (on Windows: venv\Scripts\activate)
pip install --upgrade pip
pip install -r requirements.txt
```

After installing dependencies, you can setup the Django Project.

```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Corpus depends on PostgreSQL. You might have it setup on your local system, or running it as a Docker container. Please make sure that you edit your environment variables accordingly so that proper configurations are set. You may also change the `ENVIRONMENT` to `DEVELOPMENT` to ensure that you have the Django debugging features available.

_--- Made and maintained by the Corpus team, IEEE NITK ---_
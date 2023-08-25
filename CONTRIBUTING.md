## Development Instructions

Versions for all the languages used in the project can be found in the `.tool-versions` file. Support will be provided for all Unix (MacOS, Debian/Ubuntu) based systems. If you choose to develop on Windows, we cannot promise anything xD. We also will not be supporting RHEL-based operating systems.

If you do not have access to a Unix machine, Docker is the recommended way for development.

### Pre Commit Hooks

We maintain code quality using pre-commit hooks (defined in [.pre-commit-config.yaml](.pre-commit-config.yaml)). All developers are requested to install all the pre-commit hooks before making any contributions to the codebase. Read more about pre-commit hooks [here](https://pre-commit.com/).

To install pre-commit hooks, run the following commands:

```shell
# Install the pre-commit framework
pip install pre-commit

# Install the pre-commit hooks
pre-commit install
```

### Docker Development

This is the preferred way for development. All modern editors allow you to open code in Docker containers remotely. If that is not possible, all code is mounted to Docker containers, so you can make changes that can be checked live.

For development, use the development Docker Compose file.

```shell
cp env.example .env

# Make required changes to the .env file

docker compose up --build
```

This Compose file will mount your codebase for dynamic updation.

## Working on the Local System

If you do not want to use Docker, you can do so by setting up the project locally. Ensure that you fetch the proper environment variables before doing so.

```shell
set -a
source .env
```

Apart from this, you will also have to set the `ENVIRONMENT` variable, which can be set to `DEVELOPMENT`.

Corpus depends on PostgreSQL. You might have it setup on your local system, or running it as a Docker container. Please make sure that you edit your environment variables accordingly so that proper configurations are set. You may also change the `ENVIRONMENT` to `DEVELOPMENT` to ensure that you have the Django debugging features available.

The application is a Django app. The recommended approach is to create a Python virtual environment, and setup the project (if you are using `conda`, please refer to that documentation for instructions).

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

# IEEE NITK Corpus

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/IEEE-NITK/corpus/main.svg)](https://results.pre-commit.ci/latest/github/IEEE-NITK/corpus/main)

A Django based web application to manage all things IEEE NITK.

## Setup Instructions

1. Run the following command to create a copy of the environment file. Change the environment variables as necessary in the copied file.

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

## Production Setup
For production setup, use the production docker compose file.

```sh
docker compose -f prod-docker-compose.yml up --build
```

## Contributing
Refer to the [contribution](./CONTRIBUTING.md) guidelines for more information about how to set the project locally for development and contribution.

_--- Made and maintained by the Corpus team, IEEE NITK ---_

# IEEE NITK Corpus

A Django based web application to manage all things IEEE NITK.

## Setup Instructions

1. Run the following command to create a copy of the environment file.

```sh
cp .env.example .env
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
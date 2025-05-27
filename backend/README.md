# Backend

This folder contains the backend for Corpus, IEEE NITK

## Setup
This project has dependencies managed by [`uv`](https://docs.astral.sh/uv/). Please install it if you do not have it.
You can setup the project using the following steps:

```shell
# Create environment file
cp example.env .env

# Run necessary services (like DB)
docker compose up --build

# Load environment variables to current session
set -a
source .env

# Run the background project

cd backend/
uv sync
uv run manage.py runserver
```
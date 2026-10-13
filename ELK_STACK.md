# ELK Stack for Corpus: A Beginner's Guide

This guide explains how to add **centralised logging** to Corpus with the **ELK stack** (Elasticsearch, Logstash, Kibana), plus a small helper called **Filebeat**.

It is written for someone who has **never used ELK before**. If you know Django and have run `docker compose up` for this project, you have everything you need. The guide explains each idea before it uses it.

> **What you will have at the end**
>
> - Every log line from Django, Celery, PostgreSQL, Redis and nginx collected in one place.
> - A web dashboard (Kibana) where you can search logs ("show me every 500 error on `/blog` in the last hour") and draw charts (requests per minute, slowest pages, top 404s).
> - A setup that is **opt-in** for development: the normal `docker compose up` keeps working exactly as before.
> - A production recipe with passwords, memory limits, Kibana behind nginx, and automatic deletion of old logs.

---:lua vim.print(vim.lsp.get_clients({bufnr=0}))

## TL;DR (for the impatient)

If you just want to see it running on your machine:

```bash
# 0. One-time machine setup (Linux / WSL2). Explained in section 3.2.
sudo sysctl -w vm.max_map_count=262144

# 1. Make the changes in sections 5 to 8 (Django logging + the elk/ config files).

# 2. Start Elasticsearch first and load the index template (section 9).
docker compose -f docker-compose.yml -f docker-compose.elk.yml up -d elasticsearch
curl -X PUT localhost:9200/_ilm/policy/corpus-logs-retention -H 'Content-Type: application/json' -d @elk/elasticsearch/ilm-policy.json
curl -X PUT localhost:9200/_index_template/corpus-logs -H 'Content-Type: application/json' -d @elk/elasticsearch/index-template.json

# 3. Start everything else.
docker compose -f docker-compose.yml -f docker-compose.elk.yml up -d --build

# 4. Visit http://localhost:8000 a few times, then open Kibana:
#    http://localhost:5601  ->  Discover  ->  create data view "corpus-logs-*"
```

---

## Table of contents

1. [Why does Corpus need this?](#1-why-does-corpus-need-this)
2. [What is the ELK stack?](#2-what-is-the-elk-stack)
3. [Before you start](#3-before-you-start)
4. [How ELK will fit into Corpus](#4-how-elk-will-fit-into-corpus)
5. [Step 1: Make Django write useful logs](#5-step-1-make-django-write-useful-logs)
6. [Step 2: Create the folder layout](#6-step-2-create-the-folder-layout)
7. [Step 3: Add environment variables](#7-step-3-add-environment-variables)
8. [Step 4: Write the ELK config files](#8-step-4-write-the-elk-config-files)
9. [Step 5: Start everything and check it works](#9-step-5-start-everything-and-check-it-works)
10. [Step 6: Explore your logs in Kibana](#10-step-6-explore-your-logs-in-kibana)
11. [Step 7: Run ELK in production](#11-step-7-run-elk-in-production)
12. [Troubleshooting](#12-troubleshooting)
13. [Stopping and cleaning up](#13-stopping-and-cleaning-up)
14. [Command cheat sheet](#14-command-cheat-sheet)
15. [Where to go next](#15-where-to-go-next)
16. [Final checklist](#16-final-checklist)

---

## 1. Why does Corpus need this?

Corpus runs as several Docker containers. In development ([docker-compose.yml](docker-compose.yml)) these are:

| Service       | What it does                                        | What its logs tell you                         |
| ------------- | --------------------------------------------------- | ---------------------------------------------- |
| `corpus`      | The Django web app                                  | Requests, errors, warnings from our code       |
| `celery`      | Background task worker (emails, etc.)               | Which tasks ran, which failed, and why         |
| `postgres`    | The database                                        | Slow queries, connection errors, crashes       |
| `redis`       | Message broker for Celery                           | Memory warnings, restarts                      |
| `adminer`     | Database admin UI                                   | Not very interesting                           |
| `jstoolchain` | Tailwind CSS watcher                                | Build output (noise for our purposes)          |

In production ([prod-docker-compose.yml](prod-docker-compose.yml)) there is also `nginx` (the front door that receives every request from the internet) and `certbot`.

Today, to understand a problem you have to do something like this:

```bash
docker compose logs corpus | grep -i error
docker compose logs postgres | tail -100
```

This works for small problems, but it breaks down quickly:

- **Logs are scattered.** A failed newsletter email might involve `corpus`, `celery` and `redis`, and you have to look in three places.
- **You can't search well.** `grep` cannot answer "which pages returned 500 errors yesterday between 6 and 8 pm?".
- **You can't see trends.** "Are we getting more 404s since the redesign?" is impossible to answer by reading text.
- **Logs disappear.** When a container is recreated, its old logs are gone.
- **Our Django app barely logs anything right now.** [corpus/corpus/settings.py](corpus/corpus/settings.py) has no `LOGGING` setting, and the code uses `print()` in a few places. In production (where `DEBUG` is off), Django's default setup prints almost nothing.

The ELK stack fixes all of these. It collects logs from every container, stores them in a searchable database, and gives you a web UI to explore them.

---

## 2. What is the ELK stack?

**ELK** is an acronym for three open-source tools made by the company Elastic:

- **E**lasticsearch
- **L**ogstash
- **K**ibana

Later Elastic added a family of small "shipper" programs called **Beats**. We use one of them, **Filebeat**. Because of this, people sometimes call the whole thing the **Elastic Stack**. "ELK" and "Elastic Stack" mean the same thing in practice.

All of them are free to run yourself.

### 2.1 The four pieces, explained with an analogy

Imagine a library that receives thousands of letters per day.

| Piece             | Analogy                                                                                                    | What it really does                                                                                                                                                     |
| ----------------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Filebeat**      | The **postman**. Picks up letters from every house and delivers them. Light and cheap.                      | A tiny program that watches log files (here, Docker's log files), reads every new line, and sends it onwards. It remembers where it stopped, so nothing is lost or sent twice. |
| **Logstash**      | The **sorting office**. Opens each letter, reads it, stamps a date on it, sorts it into the right pile.     | A processing pipeline. It receives raw log lines, **parses** them (turns text into structured fields like `status_code: 500`), cleans them up, and forwards them.         |
| **Elasticsearch** | The **library with a perfect index**. Stores every letter and can find any of them in milliseconds.        | A search engine and database. It stores each log line as a JSON **document** and builds indexes, so searching millions of lines is fast.                                |
| **Kibana**        | The **reading room**. A comfortable place with search terminals and wall charts.                           | A website that talks to Elasticsearch. You use it to search logs, build charts and dashboards. You never need to talk to Elasticsearch directly if you don't want to.     |

### 2.2 How a log line travels

Here is the whole journey of a single log line in our setup:

```text
  ┌──────────────────────────── Docker host (your laptop or the server) ────────────────────────────┐
  │                                                                                                  │
  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐                                │
  │  │  corpus  │ │  celery  │ │ postgres │ │  redis   │ │  nginx   │   (1) apps write logs to        │
  │  │ (Django) │ │          │ │          │ │          │ │  (prod)  │       stdout / stderr           │
  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘                                │
  │       └────────────┴────────────┼────────────┴────────────┘                                      │
  │                                 ▼                                                                │
  │              /var/lib/docker/containers/<id>/<id>-json.log    (2) Docker saves every line        │
  │                                 │                                 to a file on disk              │
  │                                 ▼                                                                │
  │                          ┌─────────────┐                                                         │
  │                          │  Filebeat   │   (3) reads the files, adds container name etc.         │
  │                          └──────┬──────┘                                                         │
  │                                 │  port 5044                                                     │
  │                                 ▼                                                                │
  │                          ┌─────────────┐                                                         │
  │                          │  Logstash   │   (4) parses JSON / text into fields                    │
  │                          └──────┬──────┘                                                         │
  │                                 │  port 9200                                                     │
  │                                 ▼                                                                │
  │                          ┌───────────────┐                                                       │
  │                          │ Elasticsearch │ (5) stores and indexes, one index per day             │
  │                          └──────┬────────┘                                                       │
  │                                 │                                                                │
  │                                 ▼                                                                │
  │                          ┌─────────────┐                                                         │
  │                          │   Kibana    │   (6) web UI on port 5601                               │
  │                          └──────┬──────┘                                                         │
  └─────────────────────────────────┼────────────────────────────────────────────────────────────────┘
                                    ▼
                                  You 🙂  (browser)
```

Let's follow one real request: someone opens `/blog/`.

**(1) Django writes a line to stdout.** With the setup in section 5, it looks like this (one line, shown wrapped for reading):

```json
{"level": "INFO", "logger": "corpus.requests", "module": "middleware",
 "message": "GET /blog/ 200", "method": "GET", "path": "/blog/",
 "status_code": 200, "duration_ms": 41.7, "user_id": null,
 "client_ip": "172.18.0.1", "timestamp": "2026-10-01T05:12:01.123456+00:00"}
```

**(2) Docker saves it to a file**, wrapped in its own little JSON envelope:

```json
{"log":"{\"level\": \"INFO\", \"logger\": \"corpus.requests\", ...}\n","stream":"stderr","time":"2026-10-01T05:12:01.124Z"}
```

**(3) Filebeat reads the file**, unwraps Docker's envelope, and adds facts about the container: its name, its image, and which Compose service it belongs to (`corpus`).

**(4) Logstash notices it came from the `corpus` service**, sees that the message is JSON, and turns every key into a real field.

**(5) Elasticsearch stores the final document** in today's index, `corpus-logs-2026.10.01`:

```json
{
  "@timestamp": "2026-10-01T05:12:01.123Z",
  "service": "corpus",
  "level": "INFO",
  "logger": "corpus.requests",
  "message": "GET /blog/ 200",
  "method": "GET",
  "path": "/blog/",
  "status_code": 200,
  "duration_ms": 41.7,
  "user_id": null,
  "client_ip": "172.18.0.1",
  "stream": "stderr",
  "container": {
    "name": "mycorpus-corpus-1",
    "labels": { "com_docker_compose_service": "corpus" }
  }
}
```

**(6) In Kibana**, you can now type `status_code >= 500 and path : /blog*` and instantly see matching lines.

### 2.3 Words you will see (glossary)

Keep this table handy. You do not need to memorise it now.

| Term                         | Meaning                                                                                                                                                               |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Log / log line / event**   | One message written by a program, for example `GET /blog/ 200`.                                                                                                         |
| **Log level**                | How important a message is: `DEBUG` < `INFO` < `WARNING` < `ERROR` < `CRITICAL`. See section 5.1.                                                                      |
| **Structured log / JSON log**| A log line written as JSON (`{"level": "INFO", "path": "/blog/"}`) instead of free text. Machines can read it without guessing.                                         |
| **stdout / stderr**          | The two "output pipes" every program has. Docker captures both. Python's `logging` writes to stderr by default.                                                       |
| **Document**                 | One stored record in Elasticsearch. For us, one log line = one document. It is just JSON.                                                                              |
| **Field**                    | One key in a document, like `status_code` or `path`.                                                                                                                   |
| **Index**                    | A collection of documents, similar to a table in PostgreSQL. We create one per day: `corpus-logs-2026.10.01`.                                                          |
| **Mapping**                  | The "schema" of an index: which fields exist and their types (`keyword`, `text`, `integer`, ...). Elasticsearch guesses it if you don't set it.                        |
| **`keyword` vs `text`**      | `keyword` = stored exactly as-is, good for filtering and charts (`service`, `path`). `text` = split into words, good for full-text search (`message`).                  |
| **Index template**           | A rule that says "every new index whose name matches `corpus-logs-*` gets these settings and this mapping". We use one in section 9.                                   |
| **Shard / replica**          | Elasticsearch splits an index into **shards**. A **replica** is a backup copy on another server. We run one server, so we set replicas to `0`.                         |
| **Cluster health**           | `green` = all good. `yellow` = data is fine but replicas are missing (normal on one server if replicas > 0). `red` = some data is unavailable.                          |
| **ILM (Index Lifecycle Management)** | Rules for old data, for example "delete indices older than 30 days". Stops your disk from filling up.                                                          |
| **Pipeline (Logstash)**      | Logstash's config: **input** (where data comes from) → **filter** (how to change it) → **output** (where it goes).                                                     |
| **Grok**                     | A Logstash filter that pulls fields out of plain-text lines using named patterns, like a friendlier regex.                                                              |
| **Data view** (formerly *index pattern*) | Tells Kibana which indices to look at (`corpus-logs-*`) and which field is the time (`@timestamp`).                                                       |
| **Discover**                 | The Kibana page where you search and read raw log lines.                                                                                                               |
| **KQL**                      | Kibana Query Language. What you type in Kibana's search bar: `level : "ERROR" and service : "celery"`.                                                                  |
| **Lens**                     | Kibana's drag-and-drop chart builder.                                                                                                                                  |
| **`@timestamp`**             | The standard field that holds *when* the event happened. Always stored in UTC.                                                                                        |

### 2.4 ELK vs Sentry (we already have Sentry!)

Corpus already sends errors to **Sentry** in production (see the bottom of [corpus/corpus/settings.py](corpus/corpus/settings.py)). Do we still need ELK? Yes. They do different jobs:

|                         | Sentry                                         | ELK                                                       |
| ----------------------- | ---------------------------------------------- | --------------------------------------------------------- |
| What it collects        | Exceptions and errors (plus performance traces) | **Every** log line, from **every** container              |
| Best at                 | "This line of code crashed, here is the stack trace, it happened 42 times" | "What happened around 6:03 pm?", "How many 404s per day?", "What did Postgres say before the crash?" |
| Covers Postgres / nginx / Redis? | No                                     | Yes                                                       |
| Hosting                 | Sentry's cloud                                  | Self-hosted on our server                                 |

Keep both. Use Sentry to get alerted about crashes, and ELK to investigate *what led up to them*.

> **Note**
> Sentry's Python SDK automatically turns `logger.error(...)` calls into Sentry events, and attaches `INFO`/`WARNING` logs as "breadcrumbs". So when you start using `logging` properly (section 5), your Sentry reports also get better.

---

## 3. Before you start

### 3.1 Hardware and software

**Software:**

- Docker Engine 24+ (or Docker Desktop) with **Docker Compose v2**. Check with `docker compose version`.
- `curl` (for the test commands).

**Memory (RAM)** is the main cost. Elasticsearch, Logstash and Kibana run on Java / Node.js and need real memory:

| Container      | RAM we give it (dev) | Notes                                                      |
| -------------- | -------------------- | ---------------------------------------------------------- |
| Elasticsearch  | 2 GB (1 GB Java heap)| The hungry one. Will crash with less than ~1 GB.           |
| Logstash       | 1 GB (256 MB heap)   |                                                            |
| Kibana         | 1 GB                 |                                                            |
| Filebeat       | 256 MB               | Tiny.                                                      |
| **Total**      | **about 4 GB**       | On top of what Corpus already uses.                         |

So you want a machine with **at least 8 GB of RAM** for development.

> **Warning: production memory**
> In [prod-docker-compose.yml](prod-docker-compose.yml) every container is limited to `memory: 512M`. That is **far too small for Elasticsearch**. Section 11.2 explains how to give the ELK containers their own, larger limits. Check that the production server has about **4 GB of free RAM** before you start.

**WSL2 users (Windows):** WSL2 gets only a part of your computer's RAM by default. If things get killed, create or edit `C:\Users\<you>\.wslconfig`:

```ini
[wsl2]
memory=8GB
```

Then run `wsl --shutdown` in PowerShell and reopen your terminal.

### 3.2 Raise `vm.max_map_count` (Linux and WSL2)

**What:** `vm.max_map_count` is a Linux kernel setting that limits how many memory-mapped areas a program can have.

**Why:** Elasticsearch memory-maps its index files and needs many more than the default (`65530`). With the default, it may refuse to start in production mode or crash under load. The value Elastic asks for is `262144`.

**How (pick the one that matches your setup):**

```bash
# Check the current value
sysctl vm.max_map_count
```

- **Linux (and the production server).** Set it now:

  ```bash
  sudo sysctl -w vm.max_map_count=262144
  ```

  Make it survive reboots:

  ```bash
  echo "vm.max_map_count=262144" | sudo tee /etc/sysctl.d/99-elasticsearch.conf
  sudo sysctl --system
  ```

- **WSL2 with Docker installed inside your Linux distro.** Run the same `sudo sysctl -w ...` command. WSL does not always apply `/etc/sysctl.d` at boot, so to make it permanent add this to `C:\Users\<you>\.wslconfig` and run `wsl --shutdown`:

  ```ini
  [wsl2]
  kernelCommandLine = "sysctl.vm.max_map_count=262144"
  ```

- **WSL2 with Docker Desktop.** Docker Desktop runs its own hidden Linux VM. Set the value there from PowerShell:

  ```powershell
  wsl -d docker-desktop -u root sysctl -w vm.max_map_count=262144
  ```

  The `.wslconfig` line above also covers this VM, because all WSL2 distros share the same kernel.

- **macOS with Docker Desktop.** Usually already fine; nothing to do.

### 3.3 Pick one version for everything

All Elastic components **must use the same version number** (for example Elasticsearch 8.19.0 with Kibana 8.19.0). Mixing versions causes confusing errors.

We put the version in a single variable, `ELASTIC_VERSION`, in `.env` (section 7). This guide was written against the **8.19** line. Newer releases (including 9.x) use the same concepts and very similar config; check the [Elastic downloads page](https://www.elastic.co/downloads) and the release notes before upgrading.

---

## 4. How ELK will fit into Corpus

### 4.1 The approach we chose

There are several ways to get logs into Elasticsearch. We use the one that is **simplest and most robust for a Docker project**:

1. **Every app logs to stdout/stderr** (no log files inside containers).
2. **Docker already saves stdout/stderr** to a JSON file per container (that's how `docker compose logs` works).
3. **Filebeat reads those Docker files** for *all* containers.
4. **Logstash parses** the lines, with different rules per service.
5. **Elasticsearch stores** them; **Kibana shows** them.

**Why this way?**

- **Django doesn't know ELK exists.** If ELK is down, Django keeps running normally. There is no Python library talking to Elasticsearch, and no network call per log line.
- **It works for every container for free**, including Postgres, Redis and nginx, which we can't easily modify.
- **`docker compose logs` keeps working** exactly as before.
- **Development stays light.** ELK lives in a separate Compose file that you add only when you want it.

**Why Logstash and not Filebeat straight into Elasticsearch?** Filebeat *can* send directly to Elasticsearch. Logstash gives us one clear place where all the parsing rules live (JSON for Django, Grok for nginx/Postgres), which is easier to learn and change. It's also the "L" in ELK, so it's worth knowing.

### 4.2 What changes in the repository

| File                                   | New / changed | Purpose                                                       |
| -------------------------------------- | ------------- | ------------------------------------------------------------- |
| `corpus/requirements.txt`              | changed       | Add `python-json-logger`                                       |
| `corpus/corpus/settings.py`            | changed       | Add `LOGGING` config and one Celery setting                    |
| `corpus/corpus/middleware.py`          | **new**       | Logs every HTTP request with timing                            |
| `env.example`                          | changed       | ELK variables                                                  |
| `elk/filebeat/filebeat.yml`            | **new**       | Filebeat config                                                |
| `elk/logstash/pipeline/logstash.conf`  | **new**       | Logstash pipeline                                              |
| `elk/elasticsearch/ilm-policy.json`    | **new**       | "Delete logs after 30 days" rule                               |
| `elk/elasticsearch/index-template.json`| **new**       | Settings and field types for our indices                       |
| `docker-compose.elk.yml`               | **new**       | ELK services for development                                   |
| `prod-elk-docker-compose.yml`          | **new**       | ELK services for production                                    |
| `nginx/default.conf`                   | changed (prod)| Serve Kibana at `/kibana`; optional JSON access logs           |

**What does *not* change:** the existing `docker-compose.yml`, the CI workflow in [.github/workflows/django_tests.yml](.github/workflows/django_tests.yml), and the normal `docker compose up` developer experience.

---

## 5. Step 1: Make Django write useful logs

ELK can only show what our apps write. Right now, Django writes very little, so this step matters most. It is also useful **on its own**, even without ELK.

### 5.1 A 2-minute introduction to Python logging

Python has a built-in `logging` module. Instead of `print("something happened")`, you write:

```python
import logging

logger = logging.getLogger(__name__)   # __name__ is e.g. "blog.views"

logger.info("Blog post published", extra={"post_id": post.id})
```

Why is this better than `print()`?

- Every message has a **level**, so you can hide noise and keep the important bits.
- Every message has a **logger name** (like `blog.views`), so you know *where* it came from.
- You can attach **extra fields** (`post_id`) that become searchable fields in Kibana.
- One central config (`LOGGING` in `settings.py`) decides the format and destination for all messages.

**The five levels, with Corpus examples:**

| Level      | Use it when...                                          | Corpus example                                                |
| ---------- | ------------------------------------------------------- | ------------------------------------------------------------- |
| `DEBUG`    | Detailed info only useful while developing              | "Computed 14 upcoming events for the home page"               |
| `INFO`     | Normal, expected things worth recording                 | "Newsletter sent to 230 subscribers", every HTTP request       |
| `WARNING`  | Something odd, but the app handled it                   | "Login failed for an unknown account", a 404                  |
| `ERROR`    | Something failed and a user was affected                | "Could not send registration email", a 500                    |
| `CRITICAL` | The app can't continue                                  | "Database unreachable"                                        |

If the configured level is `INFO`, then `DEBUG` messages are dropped and everything from `INFO` upwards is kept.

**Logger names form a tree.** `blog.views` is a child of `blog`. Django's own messages come from loggers named `django`, `django.request`, `django.db.backends`, and so on. Configuring a parent configures its children too.

### 5.2 Install `python-json-logger`

To make logs easy for machines to read, we write them as **JSON, one object per line**. The small library `python-json-logger` adds a JSON formatter to Python's `logging`.

Add this line to [corpus/requirements.txt](corpus/requirements.txt):

```text
python-json-logger>=3.1
```

> **Note**
> The Docker images install requirements **when they are built**, so after this change you must rebuild: `docker compose up --build`.

### 5.3 Add a `LOGGING` config to `settings.py`

Add the block below to [corpus/corpus/settings.py](corpus/corpus/settings.py). A good place is right after the `DEBUG = ...` line, because it uses `DEBUG`.

```python
# Logging
# https://docs.djangoproject.com/en/5.1/topics/logging/
#
# All logs go to the console (stdout/stderr), where Docker collects them.
# - LOG_FORMAT=json -> one JSON object per line (for ELK). Default in production.
# - LOG_FORMAT=text -> human-friendly lines. Default in development.
# - DJANGO_LOG_LEVEL controls how chatty we are (DEBUG, INFO, WARNING, ERROR).

DJANGO_LOG_LEVEL = os.getenv("DJANGO_LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv("LOG_FORMAT", "text" if DEBUG else "json")

LOGGING = {
    "version": 1,
    # Keep Django's and other libraries' loggers working.
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            # "()" tells Python which class to build the formatter from.
            "()": "pythonjsonlogger.json.JsonFormatter",
            # The fields to include in every line.
            "fmt": "%(levelname)s %(name)s %(module)s %(message)s",
            # Nicer field names in Kibana.
            "rename_fields": {"levelname": "level", "name": "logger"},
            # Adds "timestamp" in ISO 8601 format, in UTC.
            "timestamp": True,
        },
        "text": {
            "format": "{asctime} {levelname:<8} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": LOG_FORMAT,
        },
    },
    # The "root" logger catches everything not configured below,
    # including all our apps (blog, accounts, newsletter, ...).
    "root": {
        "handlers": ["console"],
        "level": DJANGO_LOG_LEVEL,
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": DJANGO_LOG_LEVEL,
            "propagate": False,
        },
        # 4xx responses are logged as WARNING, 5xx as ERROR (with traceback).
        "django.request": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        # Set this to "DEBUG" to log every SQL query. Very noisy!
        "django.db.backends": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "celery": {
            "handlers": ["console"],
            "level": DJANGO_LOG_LEVEL,
            "propagate": False,
        },
    },
}
```

**What each part means:**

- **`formatters`** decide *how a line looks*. We define two (`json` and `text`) and pick one with `LOG_FORMAT`.
- **`handlers`** decide *where lines go*. We have one: the console. Docker collects the console output.
- **`root` and `loggers`** decide *which messages are kept*, by level.
- **`propagate: False`** stops a message from also being passed up to the root logger, which would print it twice.

**Why JSON only in production by default?** JSON is great for machines but hard to read in your terminal. So in development you get readable text, unless you start ELK (the ELK Compose file in section 8.4 switches `LOG_FORMAT` to `json` for you).

**What about stack traces?** With the JSON formatter, a whole traceback is stored in **one** field (`exc_info`) of **one** log line. This avoids a classic ELK headache, where a 30-line traceback becomes 30 separate, useless log entries.

### 5.4 Write logs in your own code

In any module, create a logger at the top of the file and use it:

```python
# For example in corpus/newsletter/views.py
import logging

logger = logging.getLogger(__name__)  # becomes "newsletter.views"


def some_view(request):
    ...
    logger.info("Newsletter issue sent", extra={"issue_id": issue.id, "recipients": count})
    ...
    try:
        send_the_email(...)
    except Exception:
        # logger.exception = logger.error + the full traceback
        logger.exception("Failed to send newsletter", extra={"issue_id": issue.id})
        raise
```

**Good habits:**

- **Use `extra={...}` for data**, not string formatting. `extra={"issue_id": 7}` becomes a searchable `issue_id` field in Kibana; `f"issue {7}"` is just text.
- **Use `logger.exception(...)` inside `except` blocks** so the traceback is included.
- **Replace `print()` gradually.** The codebase has about a dozen `print()` calls. Under gunicorn and Celery, prints are unstructured and have no level. Find them with:

  ```bash
  grep -rn "print(" corpus --include=*.py | grep -v migrations
  ```

> **Warning: never log secrets or personal data**
> Do not log passwords, password-reset tokens, session IDs, full email addresses, phone numbers or `request.POST` dumps. Logs are copied to more places (Elasticsearch, backups) than the database, and they're read by more people. Log IDs (`user_id`, `post_id`) instead.

**Avoid clashing field names in `extra`.** Python reserves some names (`message`, `asctime`, `module`, `name`, `levelname`, ...) and raises an error if you use them in `extra`. Use names like `post_id`, `event_slug`, `recipients`.

### 5.5 Log every request with a small middleware (recommended)

In development, `runserver` prints a line per request, but gunicorn (production) does not by default. More importantly, neither of them records **how long** the request took or **who** made it. A tiny middleware gives us one structured line per request, in every environment.

Create **`corpus/corpus/middleware.py`**:

```python
import logging
import time

logger = logging.getLogger("corpus.requests")

# Requests for these paths are not logged (they're noisy and rarely useful).
SKIP_PREFIXES = ("/static/", "/media/", "/favicon.ico")


class RequestLogMiddleware:
    """Write one log line per HTTP request, with method, path, status and timing."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(SKIP_PREFIXES):
            return self.get_response(request)

        start = time.monotonic()
        response = self.get_response(request)
        duration_ms = round((time.monotonic() - start) * 1000, 2)

        user = getattr(request, "user", None)
        logger.info(
            "%s %s %s",
            request.method,
            request.path,
            response.status_code,
            extra={
                "method": request.method,
                "path": request.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "user_id": user.pk if user is not None and user.is_authenticated else None,
                # nginx sets X-Real-IP in production (see nginx/default.conf).
                "client_ip": request.META.get("HTTP_X_REAL_IP") or request.META.get("REMOTE_ADDR"),
            },
        )
        return response
```

Then register it at the **end** of `MIDDLEWARE` in [corpus/corpus/settings.py](corpus/corpus/settings.py):

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # ... the existing entries stay as they are ...
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corpus.middleware.RequestLogMiddleware",
]
```

**How it works:** Django calls `__call__` for every request. We note the time, let the rest of Django build the response (`self.get_response(request)`), then measure the time taken and write one log line. Even when a view crashes, Django turns the crash into a 500 response before it reaches us, so 500s are logged too.

**Privacy note:** IP addresses count as personal data in many places. If you don't need them, remove the `client_ip` line.

### 5.6 Make Celery use the same format

By default, Celery **takes over** Python's logging when the worker starts, replacing our JSON setup with its own text format. Tell it not to, by adding this next to the other Celery settings in [corpus/corpus/settings.py](corpus/corpus/settings.py):

```python
# Let Django's LOGGING config control Celery's output (JSON for ELK).
CELERY_WORKER_HIJACK_ROOT_LOGGER = False
```

The `CELERY_` prefix works because [corpus/corpus/celery.py](corpus/corpus/celery.py) loads settings with `namespace='CELERY'`, so this becomes Celery's `worker_hijack_root_logger` option.

Inside tasks, log the normal way:

```python
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_welcome_email(user_id):
    logger.info("Sending welcome email", extra={"target_user_id": user_id})
```

### 5.7 Check your logging before moving on

Rebuild and start the normal stack:

```bash
docker compose up --build
```

Open <http://localhost:8000> and click around. In the `corpus` output you should now see readable lines like:

```text
2026-10-01 10:42:01,123 INFO     corpus.requests: GET / 200
2026-10-01 10:42:03,456 WARNING  django.request: Not Found: /does-not-exist
2026-10-01 10:42:03,457 INFO     corpus.requests: GET /does-not-exist 404
```

To preview the JSON format, add `LOG_FORMAT="json"` to your `.env` and restart. You should see:

```text
{"level": "INFO", "logger": "corpus.requests", "module": "middleware", "message": "GET / 200", "method": "GET", "path": "/", "status_code": 200, "duration_ms": 35.2, "user_id": null, "client_ip": "172.18.0.1", "timestamp": "2026-10-01T05:12:01.123456+00:00"}
```

> **Note**
> You will still see some plain-text lines, like `runserver`'s own `"GET / HTTP/1.1" 200` lines and gunicorn's startup messages. That's fine: Logstash stores non-JSON lines as plain text.

> **Note: tests**
> `python manage.py test` will now print `WARNING` lines such as `Not Found: /...` for tests that deliberately hit missing pages. This is expected and does not mean a test failed.

---

## 6. Step 2: Create the folder layout

All ELK configuration lives in a new top-level `elk/` folder:

```text
MyCorpus/
├── corpus/                          # the Django project (unchanged layout)
├── nginx/
├── elk/                             # NEW
│   ├── elasticsearch/
│   │   ├── ilm-policy.json          # delete logs after N days
│   │   └── index-template.json      # settings + field types for corpus-logs-*
│   ├── filebeat/
│   │   └── filebeat.yml             # what to collect, where to send it
│   └── logstash/
│       └── pipeline/
│           └── logstash.conf        # how to parse each service's logs
├── docker-compose.yml               # unchanged
├── docker-compose.elk.yml           # NEW: ELK for development
├── prod-docker-compose.yml          # unchanged
├── prod-elk-docker-compose.yml      # NEW: ELK for production
└── ELK_STACK.md                     # this guide
```

Create the folders:

```bash
mkdir -p elk/elasticsearch elk/filebeat elk/logstash/pipeline
```

Kibana and Elasticsearch themselves need no config files: we configure them with environment variables in the Compose files.

---

## 7. Step 3: Add environment variables

Add this block to the end of [env.example](env.example), and copy the same lines into your own `.env`:

```bash
# ELK Stack Settings (see ELK_STACK.md)
# All Elastic components must use the same version.
ELASTIC_VERSION="8.19.0"

# Passwords below are only used in production, where Elasticsearch security is ON.
# Generate real values with:  openssl rand -hex 24
ELASTIC_PASSWORD="change-me-elastic"
KIBANA_SYSTEM_PASSWORD="change-me-kibana"
LOGSTASH_INTERNAL_PASSWORD="change-me-logstash"
# Must be at least 32 characters. Generate with:  openssl rand -hex 32
KIBANA_ENCRYPTION_KEY="change-me-to-a-random-string-of-at-least-32-characters"

# Django logging
DJANGO_LOG_LEVEL="INFO"
# LOG_FORMAT="json"   # "json" or "text". Default: text in development, json in production.
```

**What each variable does:**

| Variable                     | Used by                    | Meaning                                                                    |
| ---------------------------- | -------------------------- | -------------------------------------------------------------------------- |
| `ELASTIC_VERSION`            | All ELK images             | The single version number for every Elastic component.                     |
| `ELASTIC_PASSWORD`           | Elasticsearch (prod)       | Password of the built-in superuser `elastic`. Also your first Kibana login.|
| `KIBANA_SYSTEM_PASSWORD`     | Kibana (prod)              | Password Kibana uses to talk to Elasticsearch (user `kibana_system`).      |
| `LOGSTASH_INTERNAL_PASSWORD` | Logstash (prod)            | Password Logstash uses to write logs (user `logstash_internal`).           |
| `KIBANA_ENCRYPTION_KEY`      | Kibana (prod)              | Encrypts saved secrets inside Kibana (needed for alerts, reports).         |
| `DJANGO_LOG_LEVEL`           | Django, Celery             | Minimum level to log.                                                      |
| `LOG_FORMAT`                 | Django, Celery             | `json` or `text` (see section 5.3).                                        |

> **Warning**
> `env.example` is committed to git, so it must only ever contain **placeholder** values. Put real passwords **only** in the `.env` file on the server. Use hex passwords (`openssl rand -hex 24`): they contain only `0-9a-f`, so they never break shell commands, JSON or YAML.

> **Tip: how Compose uses `.env`**
> Docker Compose reads the `.env` file next to the Compose file in two ways: it **substitutes** `${VARIABLE}` inside Compose files (that's how `${ELASTIC_VERSION}` in an image name works), and our services load it with `env_file: .env` as container environment variables.

---

## 8. Step 4: Write the ELK config files

For development we keep things simple: **Elasticsearch security is OFF** (no passwords) and ports are only reachable from your own machine. Section 11 turns security on for production.

### 8.1 Filebeat: collect logs from every container

Create **`elk/filebeat/filebeat.yml`**:

```yaml
# Filebeat reads the log files Docker writes for every container and sends
# each line to Logstash.
# Docs: https://www.elastic.co/guide/en/beats/filebeat/current/index.html

filebeat.inputs:
  # "filestream" is Filebeat's modern way to read files line by line.
  - type: filestream
    # A unique, stable id. Filebeat uses it to remember how far it has read.
    id: docker-container-logs
    paths:
      # Docker (json-file logging driver) writes one file per container here.
      - /var/lib/docker/containers/*/*.log
    # Skip files that haven't changed in 2 days, so the first start doesn't
    # import months of old logs.
    ignore_older: 48h
    parsers:
      # Unwrap Docker's {"log": "...", "stream": "...", "time": "..."} envelope.
      # Afterwards, the original line is in the "message" field and the
      # Docker timestamp becomes @timestamp.
      - container:
          stream: all     # read both stdout and stderr
          format: auto

processors:
  # Ask Docker (via its socket) about each container and add fields like
  # container.name, container.image.name and container.labels.*.
  # Docker Compose labels tell us the service name, e.g.
  # container.labels.com_docker_compose_service = "corpus".
  - add_docker_metadata:
      host: "unix:///var/run/docker.sock"

  # Throw away logs we don't want:
  - drop_event:
      when:
        or:
          # Containers that were not started by Docker Compose
          # (other things running on your machine).
          - not:
              has_fields: ["container.labels.com_docker_compose_service"]
          # ELK's own containers. Collecting these would create a loop:
          # Logstash logs a line -> Filebeat ships it -> Logstash logs again...
          - equals:
              container.labels.com_docker_compose_service: "elasticsearch"
          - equals:
              container.labels.com_docker_compose_service: "logstash"
          - equals:
              container.labels.com_docker_compose_service: "kibana"
          - equals:
              container.labels.com_docker_compose_service: "filebeat"
          # The Tailwind watcher is only noise.
          - equals:
              container.labels.com_docker_compose_service: "jstoolchain"

  # OPTIONAL: if you run other Compose projects on the same machine and only
  # want Corpus logs, uncomment and set your project name. It is the folder
  # name in lowercase by default (e.g. "mycorpus" or "corpus"); check it with
  #   docker inspect <container> --format '{{ index .Config.Labels "com.docker.compose.project" }}'
  # - drop_event:
  #     when:
  #       not:
  #         equals:
  #           container.labels.com_docker_compose_project: "corpus"

# Send everything to Logstash (service name "logstash" on corpus_network).
output.logstash:
  hosts: ["logstash:5044"]

# Filebeat's own logs: only warnings and errors.
logging.level: warning
```

**Things a beginner usually wonders about:**

- **Why does Filebeat read `/var/lib/docker/containers`?** That's where Docker's default `json-file` logging driver stores container output. We mount that folder into the Filebeat container as read-only (section 8.4).
- **Why does it need the Docker socket (`/var/run/docker.sock`)?** The log files are named by container **ID** (a long hex string). The socket lets Filebeat ask Docker "which container is this ID?" to get names and Compose labels. The socket is powerful (it can control Docker), so we mount it **read-only**, and only Filebeat gets it.
- **Why do the labels look like `com_docker_compose_service` with underscores?** Docker's real label is `com.docker.compose.service`. Filebeat replaces dots with underscores, because in Elasticsearch a dot means "nested field".

### 8.2 Logstash: parse each service's logs

A Logstash **pipeline** always has three sections: `input`, `filter`, `output`. Think of it as: *receive → transform → send*.

Create **`elk/logstash/pipeline/logstash.conf`**:

```ruby
# Logstash pipeline for Corpus.
# Docs: https://www.elastic.co/guide/en/logstash/current/configuration.html
#
#   input  -> receive events from Filebeat
#   filter -> parse and clean them (different rules per service)
#   output -> store them in Elasticsearch

input {
  # Filebeat connects to this port (see output.logstash in filebeat.yml).
  beats {
    port => 5044
  }
}

filter {
  # ------------------------------------------------------------------
  # 1. Add a short "service" field with the Docker Compose service name,
  #    so we can write simple searches like  service : "corpus"
  # ------------------------------------------------------------------
  if [container][labels][com_docker_compose_service] {
    mutate {
      add_field => { "service" => "%{[container][labels][com_docker_compose_service]}" }
    }
  } else {
    mutate {
      add_field => { "service" => "unknown" }
    }
  }

  # ------------------------------------------------------------------
  # 2. Django and Celery: lines that look like JSON are parsed into fields.
  #    Plain-text lines (runserver, gunicorn start-up) are kept as they are.
  # ------------------------------------------------------------------
  if [service] in ["corpus", "celery"] {
    if [message] =~ /^\s*\{/ {
      json {
        # Parse the JSON in "message" and put every key at the top level.
        # The JSON's own "message" key replaces the raw line.
        source => "message"
        skip_on_invalid_json => true
      }
      # Use the time Django wrote (more precise than Docker's) as @timestamp.
      if [timestamp] {
        date {
          match => ["timestamp", "ISO8601"]
          remove_field => ["timestamp"]
        }
      }
    }
  }

  # ------------------------------------------------------------------
  # 3. nginx (production): access logs.
  #    JSON if you enable the JSON log format (section 11.6), otherwise the
  #    standard "combined" text format, parsed with a ready-made Grok pattern.
  # ------------------------------------------------------------------
  else if [service] == "nginx" {
    if [message] =~ /^\s*\{/ {
      json {
        source => "message"
        skip_on_invalid_json => true
      }
      if [time] {
        date {
          match => ["time", "ISO8601"]
          remove_field => ["time"]
        }
      }
    } else {
      grok {
        # COMBINEDAPACHELOG understands lines like:
        # 1.2.3.4 - - [01/Oct/2026:10:00:00 +0000] "GET /blog/ HTTP/1.1" 200 5120 "-" "Mozilla/5.0 ..."
        match => { "message" => "%{COMBINEDAPACHELOG}" }
        tag_on_failure => ["_nginx_grok_failure"]
      }
    }
  }

  # ------------------------------------------------------------------
  # 4. PostgreSQL: lines look like
  #    2026-10-01 10:00:00.123 UTC [57] ERROR:  relation "foo" does not exist
  # ------------------------------------------------------------------
  else if [service] == "postgres" {
    grok {
      match => {
        "message" => "^%{TIMESTAMP_ISO8601:pg_time} %{WORD:pg_timezone} \[%{POSINT:pg_pid}\] %{WORD:level}:\s+%{GREEDYDATA:message}"
      }
      # Replace the raw line with just the text after "ERROR:".
      overwrite => ["message"]
      tag_on_failure => ["_postgres_grok_failure"]
    }
  }

  # Redis, adminer and anything else: stored as plain text. That's fine.

  # ------------------------------------------------------------------
  # 5. Clean-up for everything
  # ------------------------------------------------------------------
  if [level] {
    mutate {
      uppercase => ["level"]   # "info" and "INFO" become the same value
    }
  }

  mutate {
    # Fields Filebeat adds that we never search on.
    remove_field => ["agent", "input", "@version"]
  }
}

output {
  elasticsearch {
    # ${NAME:default} reads an environment variable, with a default value.
    # In development nothing is set, so the defaults are used. Elasticsearch
    # security is off in development, so the user/password are ignored there.
    # In production (section 11) the Compose file sets the real values.
    hosts    => ["${ELASTICSEARCH_HOSTS:http://elasticsearch:9200}"]
    user     => "${LOGSTASH_ES_USER:elastic}"
    password => "${LOGSTASH_ES_PASSWORD:unused-in-development}"

    # One index per day, e.g. corpus-logs-2026.10.01 (date is in UTC).
    index => "corpus-logs-%{+YYYY.MM.dd}"
    # Use a classic index, not a "data stream", to keep things simple.
    data_stream => "false"
    # We manage the index template ourselves (elk/elasticsearch/index-template.json).
    manage_template => false
  }

  # DEBUGGING: uncomment to also print every event in Logstash's own logs
  # (see them with: docker compose ... logs -f logstash).
  # stdout { codec => rubydebug }
}
```

**How to read this file:**

- `[container][labels][com_docker_compose_service]` is Logstash's way to write the nested field `container.labels.com_docker_compose_service`.
- `"%{[some][field]}"` inserts the value of a field into a string.
- `if [message] =~ /^\s*\{/` means "if the message starts with `{`" (a regular expression).
- **Grok patterns** like `%{WORD:level}` mean "match one word, and save it in a field called `level`". Logstash ships with hundreds of named patterns; `COMBINEDAPACHELOG` is one big ready-made pattern for web server logs.
- When Grok can't match a line, it adds a **tag** (for example `_postgres_grok_failure`) instead of losing the line. You can search for those tags in Kibana to improve your patterns.

> **Note: field names from Grok**
> Newer Logstash versions use the **Elastic Common Schema (ECS)** names for fields extracted by built-in patterns. So `COMBINEDAPACHELOG` produces fields like `source.address`, `http.request.method`, `url.original` and `http.response.status_code`, not `clientip` or `verb` as older tutorials show.

### 8.3 Elasticsearch: retention policy and index template

These two small JSON files tell Elasticsearch how to treat our indices. We load them once, in section 9.

**`elk/elasticsearch/ilm-policy.json`** deletes daily indices 30 days after they were created:

```json
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {}
      },
      "delete": {
        "min_age": "30d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

Change `"30d"` to whatever retention you want (for example `"7d"` on a small laptop).

**`elk/elasticsearch/index-template.json`** applies to every new index named `corpus-logs-*`:

```json
{
  "index_patterns": ["corpus-logs-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 0,
      "index.lifecycle.name": "corpus-logs-retention"
    },
    "mappings": {
      "properties": {
        "service":     { "type": "keyword" },
        "level":       { "type": "keyword" },
        "logger":      { "type": "keyword" },
        "module":      { "type": "keyword" },
        "method":      { "type": "keyword" },
        "path":        { "type": "keyword" },
        "status_code": { "type": "integer" },
        "duration_ms": { "type": "float" },
        "user_id":     { "type": "long" },
        "client_ip":   { "type": "keyword" },
        "message":     { "type": "text" },
        "exc_info":    { "type": "text" }
      }
    }
  }
}
```

**Why bother?**

- **`number_of_replicas: 0`**: we run a single Elasticsearch node, so there's nowhere to put a replica. Without this, cluster health stays `yellow` forever.
- **`index.lifecycle.name`**: connects every new index to the 30-day deletion policy.
- **`mappings`**: without them, Elasticsearch **guesses** each field's type from the first value it sees. Guesses can go wrong (a field becomes `text` when you wanted to filter on it, or a number gets stored as a string). Setting types for our main fields makes searches and charts reliable. Any field not listed here is still stored; Elasticsearch just guesses its type.

### 8.4 The development Compose file

Instead of editing [docker-compose.yml](docker-compose.yml), we create a second file that **adds** to it. When you pass several `-f` files, Compose merges them in order:

```bash
docker compose -f docker-compose.yml -f docker-compose.elk.yml up
```

This keeps ELK fully optional: CI and everyday development keep using `docker-compose.yml` alone.

Create **`docker-compose.elk.yml`** in the repository root:

```yaml
# ELK stack for DEVELOPMENT. Use it together with the main file:
#
#   docker compose -f docker-compose.yml -f docker-compose.elk.yml up -d --build
#
# See ELK_STACK.md for the full guide.

services:
  # --- Switch the apps to JSON logs while ELK is running --------------------
  # (These entries are merged into the services in docker-compose.yml.)
  corpus:
    environment:
      - LOG_FORMAT=json

  celery:
    environment:
      - LOG_FORMAT=json

  # --- Elasticsearch: stores and searches the logs -------------------------
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:${ELASTIC_VERSION}
    restart: unless-stopped
    environment:
      - node.name=es01
      - cluster.name=corpus-logs
      # Run as a single server; don't look for other nodes.
      - discovery.type=single-node
      # No passwords in development. NEVER do this on a public server.
      - xpack.security.enabled=false
      # Java heap: fixed at 1 GB (min = max is recommended).
      - ES_JAVA_OPTS=-Xms1g -Xmx1g
    mem_limit: 2g
    volumes:
      # Keep data when the container is recreated.
      - es_data:/usr/share/elasticsearch/data
    ports:
      # 127.0.0.1 = only reachable from this machine.
      - "127.0.0.1:9200:9200"
    networks:
      - corpus_network
    healthcheck:
      # Healthy once the cluster is at least "yellow".
      test: ["CMD-SHELL", "curl -fs 'http://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=5s' || exit 1"]
      interval: 15s
      timeout: 10s
      retries: 20
      start_period: 60s

  # --- Logstash: parses log lines -------------------------------------------
  logstash:
    image: docker.elastic.co/logstash/logstash:${ELASTIC_VERSION}
    restart: unless-stopped
    environment:
      - LS_JAVA_OPTS=-Xms256m -Xmx256m
      - XPACK_MONITORING_ENABLED=false
      # Reload logstash.conf automatically when you edit it.
      - CONFIG_RELOAD_AUTOMATIC=true
    mem_limit: 1g
    volumes:
      - ./elk/logstash/pipeline:/usr/share/logstash/pipeline:ro
    expose:
      - "5044"
    networks:
      - corpus_network
    depends_on:
      elasticsearch:
        condition: service_healthy

  # --- Kibana: the web UI ---------------------------------------------------
  kibana:
    image: docker.elastic.co/kibana/kibana:${ELASTIC_VERSION}
    restart: unless-stopped
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    mem_limit: 1g
    ports:
      - "127.0.0.1:5601:5601"
    networks:
      - corpus_network
    depends_on:
      elasticsearch:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -fs http://localhost:5601/api/status || exit 1"]
      interval: 15s
      timeout: 10s
      retries: 20
      start_period: 60s

  # --- Filebeat: ships Docker logs to Logstash ------------------------------
  filebeat:
    image: docker.elastic.co/beats/filebeat:${ELASTIC_VERSION}
    restart: unless-stopped
    # Root is needed to read Docker's log files and socket.
    user: root
    command:
      # Log to the console instead of a file.
      - -e
      # Our mounted filebeat.yml is owned by your user, not root. Without this
      # flag Filebeat refuses to load it ("config file must be owned by root").
      - --strict.perms=false
    mem_limit: 256m
    volumes:
      - ./elk/filebeat/filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      # Filebeat's memory of "how far did I read each file". Keeping it in a
      # volume avoids re-sending everything after a restart.
      - filebeat_data:/usr/share/filebeat/data
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - corpus_network
    depends_on:
      - logstash

volumes:
  es_data:
  filebeat_data:
```

**Line-by-line highlights for beginners:**

- **`image: ...:${ELASTIC_VERSION}`**: the official images from Elastic's registry, all on the same version.
- **`discovery.type=single-node`**: Elasticsearch is designed to run as a cluster of many servers. This tells it to run alone.
- **`ES_JAVA_OPTS=-Xms1g -Xmx1g`**: Java's starting and maximum memory. Elastic recommends setting both to the same value, and to no more than half of the container's memory (the rest is used by the operating system to cache files).
- **`mem_limit`**: a hard limit. If a container goes over, Docker kills it (exit code `137`).
- **`volumes: es_data`**: a named Docker volume so your logs survive `docker compose down`.
- **`ports: "127.0.0.1:9200:9200"`**: makes Elasticsearch reachable at `localhost:9200` for your `curl` commands, but **not** from other computers on your Wi-Fi. Logstash, Filebeat and Kibana reach it by service name (`elasticsearch:9200`) over `corpus_network`.
- **`depends_on ... service_healthy`**: Logstash and Kibana wait until Elasticsearch passes its health check.
- **`networks: corpus_network`**: the same network that `corpus`, `postgres` etc. use, defined in the main Compose file.

> **Tip: less typing**
> Typing two `-f` flags gets old. You can add this line to **your own** `.env` (not `env.example`, because CI uses that):
>
> ```bash
> COMPOSE_FILE=docker-compose.yml:docker-compose.elk.yml
> ```
>
> Now a plain `docker compose up` includes ELK. Remove the line to go back.

---

## 9. Step 5: Start everything and check it works

### 9.1 Start Elasticsearch on its own first

We start Elasticsearch first so we can load our index template **before** the first log arrives. A template only affects indices created *after* it exists.

```bash
docker compose -f docker-compose.yml -f docker-compose.elk.yml up -d elasticsearch
```

Wait about 30 to 60 seconds, then check that it's alive:

```bash
curl http://localhost:9200
```

Expected output (version numbers will differ):

```json
{
  "name" : "es01",
  "cluster_name" : "corpus-logs",
  "version" : {
    "number" : "8.19.0",
    ...
  },
  "tagline" : "You Know, for Search"
}
```

If you get `Connection refused` or `Empty reply`, it's still starting. Watch it with:

```bash
docker compose -f docker-compose.yml -f docker-compose.elk.yml logs -f elasticsearch
```

### 9.2 Load the retention policy and the index template

Run these from the repository root (the `@` tells `curl` to send the contents of a file):

```bash
curl -X PUT "http://localhost:9200/_ilm/policy/corpus-logs-retention" \
  -H "Content-Type: application/json" \
  -d @elk/elasticsearch/ilm-policy.json

curl -X PUT "http://localhost:9200/_index_template/corpus-logs" \
  -H "Content-Type: application/json" \
  -d @elk/elasticsearch/index-template.json
```

Both should answer:

```json
{"acknowledged":true}
```

You only need to do this once. It's stored in the `es_data` volume. If you change either JSON file later, run the command again; the change applies to the **next** day's index.

### 9.3 Start the rest

```bash
docker compose -f docker-compose.yml -f docker-compose.elk.yml up -d --build
```

Check the status of every container:

```bash
docker compose -f docker-compose.yml -f docker-compose.elk.yml ps
```

You want to see `elasticsearch` and `kibana` as `running (healthy)` and the others as `running`. Kibana takes 1 to 2 minutes to become healthy.

### 9.4 Create some logs

Open <http://localhost:8000> in your browser and:

1. Visit a few pages (home, blog, events).
2. Visit a page that doesn't exist, like <http://localhost:8000/this-does-not-exist>, to create a 404.
3. Log in and out.

### 9.5 Check that logs arrived in Elasticsearch

List our indices:

```bash
curl "http://localhost:9200/_cat/indices/corpus-logs-*?v"
```

Expected:

```text
health status index                  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   corpus-logs-2026.10.01 a1B2c3D4e5F6g7H8i9J0kL   1   0        532            0    310.2kb        310.2kb
```

- **`health green`**: thanks to `number_of_replicas: 0`.
- **`docs.count`**: the number of log lines stored. Refresh the website and run the command again; the number should grow.

Look at one stored log line:

```bash
curl "http://localhost:9200/corpus-logs-*/_search?size=1&pretty&q=service:corpus"
```

If `docs.count` stays at 0 or the index doesn't appear, go to [Troubleshooting](#12-troubleshooting). The first places to look are:

```bash
docker compose -f docker-compose.yml -f docker-compose.elk.yml logs filebeat
docker compose -f docker-compose.yml -f docker-compose.elk.yml logs logstash
```

In the Logstash logs, a healthy start ends with lines like `Pipeline started {"pipeline.id"=>"main"}` and `Starting server on port: 5044`.

---

## 10. Step 6: Explore your logs in Kibana

Open <http://localhost:5601>.

> **Note**
> If you see **"Kibana server is not ready yet"**, wait a minute and refresh. Because security is off in development, Kibana may also show a banner about security not being enabled. You can dismiss it. The exact menu names below may differ slightly between Kibana versions.

### 10.1 Create a data view

A **data view** tells Kibana which indices to read.

1. Open the menu (☰, top-left) → **Stack Management** → **Data Views** (under *Kibana*).
2. Click **Create data view**.
3. Fill in:
   - **Name:** `Corpus logs`
   - **Index pattern:** `corpus-logs-*` (the `*` matches every daily index)
   - **Timestamp field:** `@timestamp`
4. Click **Save data view to Kibana**.

### 10.2 Read logs in Discover

1. Menu (☰) → **Analytics** → **Discover**.
2. Pick the **Corpus logs** data view in the top-left dropdown.
3. Set the **time range** (top-right) to *Last 15 minutes*. If you see nothing, try a bigger range.

You'll see a histogram of how many logs arrived over time, and a list of log lines.

**Make the table readable:**

- In the field list on the left, hover over `service` and click **➕ (Add field as column)**. Do the same for `level`, `message`, `path` and `status_code`.
- Click any row's expand arrow to see **every** field of that log line, including `exc_info` (stack traces) and `container.name`.
- Click a value, then the **🔍+ / 🔍−** icons, to quickly filter "only this value" or "everything except this value".

**Timezones:** Elasticsearch stores `@timestamp` in **UTC**. Kibana shows times in **your browser's timezone** (IST for most of us), so a log written at 05:12 UTC appears as 10:42. That is correct and expected.

### 10.3 KQL cheat sheet

Type these in the search bar at the top of Discover, then press Enter.

| Goal                                         | KQL query                                                        |
| -------------------------------------------- | ---------------------------------------------------------------- |
| Only Django logs                             | `service : "corpus"`                                              |
| Only Celery logs                             | `service : "celery"`                                              |
| All errors from anywhere                     | `level : "ERROR" or level : "CRITICAL"`                           |
| Same, shorter                                | `level : ("ERROR" or "CRITICAL")`                                 |
| Server errors (HTTP 5xx)                     | `status_code >= 500`                                              |
| Pages that don't exist                       | `status_code : 404`                                               |
| Everything under `/blog`                     | `path : /blog*`                                                   |
| Slow requests (over 1 second)                | `duration_ms > 1000`                                              |
| Logs from one of our apps                    | `logger : blog.*`                                                 |
| Lines that include a stack trace             | `exc_info : *`                                                    |
| Full-text search in the message              | `message : "database"`                                            |
| Everything **except** request logs           | `not logger : "corpus.requests"`                                  |
| What a single user did                       | `user_id : 42`                                                    |
| Postgres errors                              | `service : "postgres" and level : "ERROR"`                        |
| Lines Logstash couldn't parse                | `tags : _postgres_grok_failure or tags : _nginx_grok_failure`     |

KQL basics: `field : value` means "equals", `*` is a wildcard, and you can combine conditions with `and`, `or`, `not` and parentheses.

**Save useful searches:** click **Save** (top-right in Discover) to keep a search like "All errors" so the whole team can reopen it.

### 10.4 Build your first dashboard

A **dashboard** is a page of charts that updates live. Let's build "Corpus overview".

1. Menu (☰) → **Analytics** → **Dashboards** → **Create dashboard**.
2. Click **Create visualization**. This opens **Lens**, the drag-and-drop editor. Make sure the **Corpus logs** data view is selected.

Build these four panels. After each one, click **Save and return**, then **Create visualization** again for the next.

**Panel 1: Requests over time**

- Type the query `logger : "corpus.requests"` in the Lens search bar.
- Drag **`@timestamp`** onto the chart. Lens creates a bar chart with *Count of records* over time.
- Drag **`status_code`** onto **Breakdown**. Each status (200, 302, 404, 500 ...) gets its own colour.

**Panel 2: Errors by service**

- Query: `level : ("ERROR" or "CRITICAL")`
- Chart type: **Bar vertical**. Drag **`service`** onto the horizontal axis. The vertical axis is *Count of records*.

**Panel 3: Top 404 pages**

- Query: `status_code : 404`
- Chart type: **Table**. Drag **`path`** into **Rows** (it shows the top values). The metric is *Count of records*.
- This finds broken links and old URLs that people still visit.

**Panel 4: Slowest pages**

- Query: `logger : "corpus.requests"`
- Chart type: **Table**. **Rows:** `path`. **Metrics:** click *Add or drag-and-drop a field*, choose **`duration_ms`**, then change the function to **Average** (or **95th percentile**). Sort by that column, highest first.

Finally, click **Save** at the top, name it **Corpus overview**, and set the time range to *Last 24 hours*.

### 10.5 Alerts (optional)

Kibana can run **rules** like "if there are more than 20 errors in 5 minutes, notify someone" (Menu → **Stack Management** → **Rules**). Two things to know:

- Rules need the encryption key described in section 11.3, so they're a production feature.
- On the free licence, most notification channels (email, Slack, ...) are **not** available; the free connectors mainly write to an index or to Kibana's server log. For "email me when it breaks", **Sentry is the simpler choice**, and we already have it.

---

## 11. Step 7: Run ELK in production

Development took shortcuts that are **dangerous on a public server**. This section fixes them.

### 11.1 What's different in production

| Topic          | Development                     | Production                                                            |
| -------------- | ------------------------------- | --------------------------------------------------------------------- |
| Passwords      | Security off                    | **Security on**, one user per component                               |
| Ports          | 9200 and 5601 on `127.0.0.1`    | **No ports published.** Kibana only through nginx at `/kibana`        |
| Memory         | `mem_limit`                     | `deploy.resources.limits`, like the existing prod file                 |
| Log retention  | 30 days (or less)               | 30 days, plus Docker log rotation                                      |
| Compose files  | `docker-compose.elk.yml`        | `prod-elk-docker-compose.yml`                                          |

Also note that [prod-docker-compose.yml](prod-docker-compose.yml) currently has no `celery` or `redis` services. The pipeline handles them anyway, if they're added later.

### 11.2 Memory planning

The existing production containers are each capped at 512 MB (`postgres`, `adminer`, `corpus`, `nginx`, `certbot`), so Corpus can use up to about 2.5 GB. ELK adds:

| Container     | Limit  | Java heap |
| ------------- | ------ | --------- |
| Elasticsearch | 2 GB   | 1 GB      |
| Logstash      | 1 GB   | 512 MB    |
| Kibana        | 1 GB   | n/a       |
| Filebeat      | 256 MB | n/a       |

Check free memory on the server with `free -h`. If the server has **less than about 6 GB total**, consider one of these instead:

- Run ELK on a **separate server**. Filebeat then sends to that server's Logstash over the network (use TLS).
- Use a hosted service like **Elastic Cloud**. You then run only Filebeat on our server.

Don't forget to set `vm.max_map_count` permanently on the server (section 3.2). In production it's required, not optional.

### 11.3 Users and passwords

With security on, Elasticsearch requires a username and password for every request. We use **one user per component**, so each one can do only what it needs:

| User                | Who uses it        | Can do                                       | Password variable             |
| ------------------- | ------------------ | -------------------------------------------- | ----------------------------- |
| `elastic`           | You (admin), setup | Everything (superuser)                       | `ELASTIC_PASSWORD`            |
| `kibana_system`     | Kibana             | Built-in user for Kibana's own internal data | `KIBANA_SYSTEM_PASSWORD`      |
| `logstash_internal` | Logstash           | Write to `corpus-logs-*` only                | `LOGSTASH_INTERNAL_PASSWORD`  |

On the server, put real values in `.env`:

```bash
openssl rand -hex 24   # run three times, for the three passwords
openssl rand -hex 32   # for KIBANA_ENCRYPTION_KEY
```

### 11.4 The production Compose file

Create **`prod-elk-docker-compose.yml`** in the repository root:

```yaml
# ELK stack for PRODUCTION. Use it together with the main production file:
#
#   docker compose -f prod-docker-compose.yml -f prod-elk-docker-compose.yml up -d --build
#
# First-time setup steps are in ELK_STACK.md, section 11.5.

services:
  # --- Rotate Docker log files so they don't fill the disk ------------------
  corpus:
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "5"

  nginx:
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "5"

  # --- Elasticsearch --------------------------------------------------------
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:${ELASTIC_VERSION}
    restart: always
    environment:
      - node.name=es01
      - cluster.name=corpus-logs
      - discovery.type=single-node
      # Security ON: every request needs a username and password.
      - xpack.security.enabled=true
      # Sets the password of the built-in "elastic" superuser on first start.
      - ELASTIC_PASSWORD=${ELASTIC_PASSWORD}
      - ES_JAVA_OPTS=-Xms1g -Xmx1g
    volumes:
      - es_data:/usr/share/elasticsearch/data
    # Only reachable inside corpus_network. NEVER publish 9200 to the internet.
    expose:
      - "9200"
    networks:
      - corpus_network
    healthcheck:
      # $$ = "let the container fill in this variable", not Compose.
      test: ["CMD-SHELL", "curl -fs -u elastic:$${ELASTIC_PASSWORD} 'http://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=5s' || exit 1"]
      interval: 15s
      timeout: 10s
      retries: 20
      start_period: 60s
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 2G

  # --- Logstash -------------------------------------------------------------
  logstash:
    image: docker.elastic.co/logstash/logstash:${ELASTIC_VERSION}
    restart: always
    environment:
      - LS_JAVA_OPTS=-Xms512m -Xmx512m
      - XPACK_MONITORING_ENABLED=false
      # Read by the output section of logstash.conf.
      - LOGSTASH_ES_USER=logstash_internal
      - LOGSTASH_ES_PASSWORD=${LOGSTASH_INTERNAL_PASSWORD}
    volumes:
      - ./elk/logstash/pipeline:/usr/share/logstash/pipeline:ro
    expose:
      - "5044"
    networks:
      - corpus_network
    depends_on:
      elasticsearch:
        condition: service_healthy
    deploy:
      resources:
        limits:
          cpus: "0.50"
          memory: 1G

  # --- Kibana (served by nginx at https://ieee.nitk.ac.in/kibana) -----------
  kibana:
    image: docker.elastic.co/kibana/kibana:${ELASTIC_VERSION}
    restart: always
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - ELASTICSEARCH_USERNAME=kibana_system
      - ELASTICSEARCH_PASSWORD=${KIBANA_SYSTEM_PASSWORD}
      # Kibana lives under /kibana on our domain.
      - SERVER_BASEPATH=/kibana
      - SERVER_REWRITEBASEPATH=true
      - SERVER_PUBLICBASEURL=https://ieee.nitk.ac.in/kibana
      # Encryption keys for saved objects, sessions and reports (32+ chars).
      - XPACK_ENCRYPTEDSAVEDOBJECTS_ENCRYPTIONKEY=${KIBANA_ENCRYPTION_KEY}
      - XPACK_SECURITY_ENCRYPTIONKEY=${KIBANA_ENCRYPTION_KEY}
      - XPACK_REPORTING_ENCRYPTIONKEY=${KIBANA_ENCRYPTION_KEY}
    expose:
      - "5601"
    networks:
      - corpus_network
    depends_on:
      elasticsearch:
        condition: service_healthy
    deploy:
      resources:
        limits:
          cpus: "0.50"
          memory: 1G

  # --- Filebeat -------------------------------------------------------------
  filebeat:
    image: docker.elastic.co/beats/filebeat:${ELASTIC_VERSION}
    restart: always
    user: root
    command:
      - -e
      - --strict.perms=false
    volumes:
      - ./elk/filebeat/filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - filebeat_data:/usr/share/filebeat/data
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - corpus_network
    depends_on:
      - logstash
    deploy:
      resources:
        limits:
          cpus: "0.25"
          memory: 256M

volumes:
  es_data:
  filebeat_data:
```

**What's different from the development file:**

- `xpack.security.enabled=true` plus `ELASTIC_PASSWORD`.
- `expose` instead of `ports`: the services are reachable by other containers but not from outside the server.
- Logstash gets its credentials through `LOGSTASH_ES_USER` / `LOGSTASH_ES_PASSWORD`, which the output section of `logstash.conf` already reads. **The same pipeline file works in both environments.**
- Kibana knows it lives under `/kibana` and has encryption keys.
- `deploy.resources.limits` matches the style of [prod-docker-compose.yml](prod-docker-compose.yml).
- Docker **log rotation** for `corpus` and `nginx`: without it, Docker's log files grow forever. With it, each container keeps at most 5 files of 10 MB. Filebeat handles rotated files correctly.

> **Note**
> Elasticsearch in this setup speaks plain HTTP (not HTTPS) **inside** the private Docker network, which nothing outside the server can reach. Public traffic to Kibana is encrypted by nginx with the existing Let's Encrypt certificate. If you ever move ELK to another server, you must turn on TLS between the servers.

### 11.5 First-time production setup, step by step

Run all commands on the server, in the repository folder.

**1. Load the variables from `.env` into your shell and define two shortcuts:**

```bash
set -a; source .env; set +a

DC="docker compose -f prod-docker-compose.yml -f prod-elk-docker-compose.yml"

# es <METHOD> <PATH> [curl options] : talk to Elasticsearch as the "elastic" superuser
es() {
  local method=$1 path=$2; shift 2
  $DC exec -T elasticsearch curl -s -u "elastic:${ELASTIC_PASSWORD}" \
    -H "Content-Type: application/json" -X "$method" "http://localhost:9200$path" "$@"
}
```

Because port 9200 isn't published in production, the `es` shortcut runs `curl` **inside** the Elasticsearch container.

**2. Start only Elasticsearch, and wait until it's healthy:**

```bash
$DC up -d elasticsearch
$DC ps elasticsearch      # repeat until it shows "(healthy)"
es GET /                  # should print the "You Know, for Search" JSON
```

**3. Set the password of the built-in `kibana_system` user:**

```bash
es POST /_security/user/kibana_system/_password -d "{\"password\": \"${KIBANA_SYSTEM_PASSWORD}\"}"
```

Expected: `{}` (an empty answer means success).

**4. Create a role and a user for Logstash:**

```bash
# A role that may only write to corpus-logs-* indices
es PUT /_security/role/logstash_writer -d '{
  "cluster": ["monitor", "manage_index_templates", "manage_ilm"],
  "indices": [
    {
      "names": ["corpus-logs-*"],
      "privileges": ["write", "create", "create_index", "manage", "manage_ilm"]
    }
  ]
}'

# The user Logstash logs in as
es PUT /_security/user/logstash_internal -d "{
  \"password\": \"${LOGSTASH_INTERNAL_PASSWORD}\",
  \"roles\": [\"logstash_writer\"],
  \"full_name\": \"Internal Logstash user\"
}"
```

Expected: `{"role":{"created":true}}` and `{"created":true}`.

**5. Load the retention policy and index template** (same files as in development). `-d @-` means "read the body from standard input":

```bash
es PUT /_ilm/policy/corpus-logs-retention -d @- < elk/elasticsearch/ilm-policy.json
es PUT /_index_template/corpus-logs        -d @- < elk/elasticsearch/index-template.json
```

**6. Start everything:**

```bash
$DC up -d --build
$DC ps
```

**7. Add Kibana to nginx** (next section), then rebuild nginx:

```bash
$DC up -d --build nginx
```

**8. Log in** at <https://ieee.nitk.ac.in/kibana> as user `elastic` with your `ELASTIC_PASSWORD`. Then create the data view (section 10.1).

**9. Create personal accounts.** Don't share the `elastic` superuser. Go to Menu → **Stack Management** → **Users** → **Create user**, and give team members the built-in **`viewer`** role (read-only) or **`editor`** role (can build dashboards).

### 11.6 Serve Kibana through nginx

Add this block inside the `server { listen 443 ssl; ... }` block of [nginx/default.conf](nginx/default.conf), next to the existing `location /adminer` block:

```nginx
    location /kibana {
        # Docker's internal DNS server. Looking up "kibana" at request time
        # (instead of at start-up) means nginx still starts if Kibana is down.
        resolver 127.0.0.11 valid=30s;
        set $kibana_upstream http://kibana:5601;
        proxy_pass $kibana_upstream;

        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
```

**Why the `resolver` / `set` trick?** With a plain `proxy_pass http://kibana:5601;`, nginx looks up the name `kibana` once at start-up and **refuses to start** if it can't find it, which would take the whole website down whenever ELK isn't running. Using a variable makes nginx look it up per request instead.

**Why no path after `5601`?** Kibana was told (`SERVER_REWRITEBASEPATH=true`) to expect URLs that start with `/kibana`, so nginx passes the URL through unchanged.

**Optional: extra protection.** Kibana already has a login page. To also limit who can even see it, you can allow only certain IP ranges inside the block:

```nginx
        allow 10.0.0.0/8;     # example: campus network
        deny all;
```

### 11.7 Optional: nginx access logs as JSON

nginx's default log format is plain text, which our pipeline parses with Grok. Writing JSON directly is more reliable and gives us the same field names as Django (`path`, `status_code`).

At the **very top** of [nginx/default.conf](nginx/default.conf), outside both `server` blocks, add:

```nginx
log_format json_combined escape=json
  '{'
    '"time":"$time_iso8601",'
    '"remote_addr":"$remote_addr",'
    '"x_forwarded_for":"$http_x_forwarded_for",'
    '"method":"$request_method",'
    '"path":"$request_uri",'
    '"status_code":$status,'
    '"body_bytes_sent":$body_bytes_sent,'
    '"request_time":$request_time,'
    '"upstream_response_time":"$upstream_response_time",'
    '"referer":"$http_referer",'
    '"user_agent":"$http_user_agent"'
  '}';
```

Then add this line inside **each** `server { ... }` block:

```nginx
    access_log /var/log/nginx/access.log json_combined;
```

The official nginx image links `/var/log/nginx/access.log` to stdout, so Docker (and therefore Filebeat) still sees every line. The Logstash pipeline (section 8.2) already detects the JSON and parses it.

> **Note**
> `access_log` goes **inside** the `server` blocks on purpose. The main `nginx.conf` already has an `access_log` line; if we added another at the same level, nginx would write every request **twice**, in both formats.

### 11.8 Data retention and backups

- **Retention:** the ILM policy deletes each daily index 30 days after it was created. Check that it's working:

  ```bash
  es GET "/corpus-logs-*/_ilm/explain?pretty"
  ```

- **Disk space:** check usage regularly:

  ```bash
  es GET "/_cat/allocation?v"
  es GET "/_cat/indices/corpus-logs-*?v&s=index"
  ```

  Elasticsearch stops writing when the disk is about 95% full (see Troubleshooting).

- **Backups:** logs are usually less precious than the PostgreSQL database. If you do want backups, Elasticsearch has **snapshots** (see "Snapshot and restore" in the Elastic docs). Snapshots need a storage location such as a mounted folder or S3.

### 11.9 Production checklist

- [ ] `vm.max_map_count=262144` set permanently on the server
- [ ] At least 4 GB of free RAM for ELK
- [ ] Real, random passwords in the server's `.env` (never in git)
- [ ] `kibana_system` password set, and the `logstash_writer` role and `logstash_internal` user created
- [ ] ILM policy and index template loaded **before** the first logs arrive
- [ ] Ports 9200, 5044 and 5601 **not** reachable from the internet (check with `nmap` or `curl` from your laptop)
- [ ] Kibana works at `https://ieee.nitk.ac.in/kibana`, and team members have personal `viewer`/`editor` accounts
- [ ] Docker log rotation enabled for `corpus` and `nginx`

---

## 12. Troubleshooting

Always start with the logs of the component that seems broken:

```bash
docker compose -f docker-compose.yml -f docker-compose.elk.yml logs --tail=100 <elasticsearch|logstash|kibana|filebeat>
```

| Symptom                                                                                     | Likely cause                                                                                  | Fix                                                                                                                                                                                                             |
| ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `invalid reference format` when starting                                                    | `ELASTIC_VERSION` isn't set, so the image name ends in `:`                                    | Add `ELASTIC_VERSION` to `.env` (section 7).                                                                                                                                                                     |
| Elasticsearch exits with code **137**                                                       | Killed for using too much memory                                                              | Raise `mem_limit` / the memory limit, or give WSL2 more RAM (section 3.1). Keep the heap (`-Xmx`) at about half the limit.                                                                                       |
| `max virtual memory areas vm.max_map_count [65530] is too low`                               | Kernel setting not raised                                                                     | Section 3.2. On Docker Desktop, set it inside the `docker-desktop` VM.                                                                                                                                           |
| `curl localhost:9200` → `Connection refused` / `Empty reply from server`                    | Still starting, or it crashed                                                                 | Wait 60 s, then check `logs elasticsearch`.                                                                                                                                                                       |
| Kibana: **"Kibana server is not ready yet"** for several minutes                            | Kibana can't reach Elasticsearch, or (prod) wrong `kibana_system` password                    | Check `logs kibana` for `Unable to retrieve version information` or `security_exception`. In prod, repeat step 3 of section 11.5.                                                                               |
| No `corpus-logs-*` index appears                                                            | Filebeat isn't reading files, or Logstash can't write                                         | 1) `logs filebeat`: look for `permission denied` or `connection refused`. 2) `logs logstash`: look for `Could not index event` or `401`. 3) Uncomment `stdout { codec => rubydebug }` to see what Logstash receives. |
| Filebeat: `config file ("filebeat.yml") must be owned by the user identifier (uid=0) or root` | Normal with a bind-mounted file                                                               | Keep `--strict.perms=false` in the `command`.                                                                                                                                                                    |
| Filebeat: `permission denied` on `/var/lib/docker/containers`                               | Not running as root, or Docker uses another log driver / path                                | Keep `user: root`. Check the driver: `docker inspect <container> --format '{{.HostConfig.LogConfig.Type}}'` must print `json-file`.                                                                               |
| Logs arrive but `container.*` fields and `service` are missing (`service: unknown`)         | Filebeat can't use the Docker socket                                                          | Check the `/var/run/docker.sock` mount. On Docker Desktop, make sure the socket is enabled in Settings → Advanced.                                                                                               |
| Django logs show up as one big `message` string, with no `level`/`path` fields              | Django is writing text, not JSON                                                              | Make sure `LOG_FORMAT=json` reaches the container (`docker compose ... exec corpus env | grep LOG_FORMAT`) and that you rebuilt after adding `python-json-logger`.                                                 |
| Events tagged `_nginx_grok_failure` / `_postgres_grok_failure`                              | A line didn't match the Grok pattern                                                          | Expected for some lines (nginx error log, multi-line Postgres statements). Test patterns in Kibana: Menu → **Dev Tools** → **Grok Debugger**.                                                                    |
| Logstash: `401 Unauthorized` or `security_exception` (prod)                                 | Wrong `logstash_internal` password or missing role                                            | Repeat step 4 of section 11.5 and check `LOGSTASH_INTERNAL_PASSWORD` in `.env`.                                                                                                                                   |
| Cluster health is `yellow`                                                                  | Indices with replicas on a single-node cluster                                               | Load the index template (section 9.2). For an existing index: `curl -X PUT localhost:9200/<index>/_settings -H 'Content-Type: application/json' -d '{"index":{"number_of_replicas":0}}'`.                       |
| Kibana shows a **conflict** warning on a field                                              | The same field has different types in different indices                                       | Add the field to the `mappings` in `index-template.json`. New indices will be consistent; old ones expire after 30 days.                                                                                         |
| Times in Kibana look 5½ hours "off"                                                         | Nothing is wrong: storage is UTC, display is in your browser's timezone                       | To change the display: Stack Management → Advanced Settings → `dateFormat:tz`.                                                                                                                                    |
| `index [...] blocked by: [FORBIDDEN/12/index read-only / allow delete (api)]`               | The disk is over about 95% full, so Elasticsearch stopped writing                            | Free disk space (delete old indices, lower the ILM `min_age`, `docker system prune`). The block is removed automatically once usage drops.                                                                        |
| Laptop is slow / fans spinning                                                              | ELK is heavy                                                                                  | Run ELK only when you need it: `docker compose -f docker-compose.yml -f docker-compose.elk.yml stop elasticsearch logstash kibana filebeat`.                                                                    |
| `nginx: [emerg] host not found in upstream "kibana"`                                       | nginx can't find Kibana at start-up                                                           | Use the `resolver` + `set $kibana_upstream` version from section 11.6.                                                                                                                                           |

---

## 13. Stopping and cleaning up

**Stop everything, but keep the data:**

```bash
docker compose -f docker-compose.yml -f docker-compose.elk.yml down
```

**Stop only ELK** and keep Corpus running:

```bash
docker compose -f docker-compose.yml -f docker-compose.elk.yml stop elasticsearch logstash kibana filebeat
```

**Delete all stored logs** (this cannot be undone):

```bash
docker compose -f docker-compose.yml -f docker-compose.elk.yml down
docker volume ls | grep es_data              # find the full name, e.g. mycorpus_es_data
docker volume rm mycorpus_es_data mycorpus_filebeat_data
```

> **Warning: be careful with `down -v`**
> `docker compose ... down -v` deletes **all** volumes of the project, including **`postgres_data`, your local database**. To delete only the logs, remove the ELK volumes by name as shown above.

**Delete a single day of logs:**

```bash
curl -X DELETE "http://localhost:9200/corpus-logs-2026.10.01"
```

Elasticsearch refuses wildcard deletes like `corpus-logs-*` by default, which protects you from accidents. Name the index exactly.

---

## 14. Command cheat sheet

```bash
# Shortcut for development
DC="docker compose -f docker-compose.yml -f docker-compose.elk.yml"

$DC up -d --build                         # start everything
$DC ps                                    # status of all containers
$DC logs -f logstash                      # follow one component's logs
$DC restart filebeat                      # restart one component
$DC stop elasticsearch logstash kibana filebeat   # pause ELK, keep Corpus

curl localhost:9200                                   # is Elasticsearch up?
curl "localhost:9200/_cluster/health?pretty"          # green / yellow / red
curl "localhost:9200/_cat/indices/corpus-logs-*?v"    # list log indices and sizes
curl "localhost:9200/corpus-logs-*/_count?q=level:ERROR"            # count errors
curl "localhost:9200/corpus-logs-*/_search?size=3&pretty&q=status_code:500"  # latest 500s

# Open Kibana: http://localhost:5601
```

You can also run Elasticsearch requests from Kibana: Menu → **Dev Tools** → **Console**. Type, for example, `GET _cat/indices?v` and press ▶.

---

## 15. Where to go next

Once the basics work, here are useful next steps, roughly in order of value:

1. **Add `logger` calls to important flows**: registrations, newsletter sends, event sign-ups, admin actions. Good logs are what make ELK useful.
2. **Metricbeat**: a sibling of Filebeat that collects **metrics** (CPU, memory, Postgres connections, Redis memory) rather than logs. It has ready-made dashboards.
3. **Elastic APM**: the `elastic-apm` Python package traces each Django request (which SQL queries ran, how long each took). It needs an extra APM Server component. It overlaps with Sentry's performance tracing, so decide which one you want.
4. **Kibana Spaces and roles**: separate dashboards per team, with fine-grained access.
5. **Learn more:**
   - [Elastic Stack overview](https://www.elastic.co/elastic-stack)
   - [Running Elasticsearch with Docker](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)
   - [Filebeat: filestream input](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-input-filestream.html)
   - [Filebeat: add_docker_metadata](https://www.elastic.co/guide/en/beats/filebeat/current/add-docker-metadata.html)
   - [Logstash: configuration structure](https://www.elastic.co/guide/en/logstash/current/configuration-file-structure.html)
   - [Logstash: Grok filter](https://www.elastic.co/guide/en/logstash/current/plugins-filters-grok.html)
   - [Kibana Query Language (KQL)](https://www.elastic.co/guide/en/kibana/current/kuery-query.html)
   - [Index lifecycle management](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html)
   - [Django logging documentation](https://docs.djangoproject.com/en/5.1/topics/logging/)
   - [python-json-logger](https://github.com/nhairs/python-json-logger)

---

## 16. Final checklist

**Django (section 5)**

- [ ] `python-json-logger` added to `corpus/requirements.txt`
- [ ] `LOGGING` config added to `settings.py`
- [ ] `RequestLogMiddleware` created and added to the end of `MIDDLEWARE`
- [ ] `CELERY_WORKER_HIJACK_ROOT_LOGGER = False` added
- [ ] `docker compose up --build` shows readable log lines; `LOG_FORMAT=json` shows JSON lines

**ELK files (sections 6 to 8)**

- [ ] `elk/filebeat/filebeat.yml`
- [ ] `elk/logstash/pipeline/logstash.conf`
- [ ] `elk/elasticsearch/ilm-policy.json` and `elk/elasticsearch/index-template.json`
- [ ] `docker-compose.elk.yml`
- [ ] ELK variables added to `env.example` and your `.env`

**Running it (sections 9 and 10)**

- [ ] `vm.max_map_count` raised
- [ ] Elasticsearch answers on `localhost:9200`
- [ ] ILM policy and index template loaded (`"acknowledged":true`)
- [ ] `corpus-logs-YYYY.MM.DD` index appears with a growing `docs.count`
- [ ] Data view `corpus-logs-*` created in Kibana
- [ ] You can find your own 404 with `status_code : 404` in Discover
- [ ] "Corpus overview" dashboard saved

**Production (section 11)**: see the checklist in section 11.9.

---

_Questions or improvements? Open an issue or PR. This guide is maintained alongside the code, so please update it whenever you change the ELK setup._

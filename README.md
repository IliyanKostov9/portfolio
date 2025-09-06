# 📝 Portfolio Django app 📝

[![License](https://img.shields.io/github/license/IliyanKostov9/portfolio)](https://www.gnu.org/licenses/gpl-3.0.en.html)
[![Dependabot Updates](https://github.com/IliyanKostov9/portfolio/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/IliyanKostov9/portfolio/actions/workflows/dependabot/dependabot-updates)
[![Create and publish a Docker image](https://github.com/IliyanKostov9/portfolio/actions/workflows/docker-publish.yaml/badge.svg)](https://github.com/IliyanKostov9/portfolio/actions/workflows/docker-publish.yaml)
[![Security scanning](https://github.com/IliyanKostov9/portfolio/actions/workflows/security-scan.yaml/badge.svg)](https://github.com/IliyanKostov9/portfolio/actions/workflows/security-scan.yaml)
[![Test](https://github.com/IliyanKostov9/portfolio/actions/workflows/test.yaml/badge.svg)](https://github.com/IliyanKostov9/portfolio/actions/workflows/test.yaml)
[![GitHub release](https://img.shields.io/github/v/release/IliyanKostov9/portfolio)](#)
[![GitHub release date](https://img.shields.io/github/release-date/IliyanKostov9/portfolio)](#)
[![itHub last commit](https://img.shields.io/github/last-commit/IliyanKostov9/portfolio)](#)

## 🚀 About

This project is for creating and maintaining my personal website at [https://portfolio.ikostov.org](https://portfolio.ikostov.org).

The project is build as a server side web app with the [Django framework](https://www.djangoproject.com/).
It uses the standard (MVC) architecture pattern and the views are rendered as [Jinja templates](https://jinja.palletsprojects.com/en/stable/).

> [!IMPORTANT]
> The application follows the [Django guide deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/), however if you find any security vulnerabilities during your interaction with the prod version with the app (or just by looking at the code), then please contact me by following the [SECURITY.md](https://github.com/IliyanKostov9/portfolio/blob/master/.github/SECURITY.md) guide.

Since the application is light and only loads static data from [these yaml files](https://github.com/IliyanKostov9/portfolio/tree/master/src/apps/landing_page/config/portfolio), it currently uses [SQLite](https://sqlite.org/) (*the simpler the better*).
Email sending is done with [AWS SES](https://aws.amazon.com/ses/).

For the web server, it uses the better ASGI web server on [Uvicorn](https://www.uvicorn.org/). We don't need to run it on [Guvicorn](https://gunicorn.org/), as it doesn't get a lot of web traffic.

Testing is written with the Django integrated test suite libraries, with unit tests on the [models](https://github.com/IliyanKostov9/portfolio/tree/master/src/apps/landing_page/tests/models) and integration tests for the [views](https://github.com/IliyanKostov9/portfolio/tree/master/src/apps/landing_page/tests/views).

The development environment can be optionally installed with the help of [Nix devenv](https://devenv.sh/).
For CI/CD, it uses github action to test & scan for security vulnerabilities, for deployment is by publishing a docker image to [Github packages](https://github.com/IliyanKostov9/portfolio/pkgs/container/portfolio).
Afterwards the image gets pulled from Raspberry PI 4B and finally gets exposed to the public internet via HTTP proxy [traefik](https://traefik.io/traefik) (you can find it's configuration [here](https://github.com/IliyanKostov9/raspberry-pi-dotfiles/blob/master/docker/personal/docker-compose.yaml)).

For maintenance it uses [Grafana](https://grafana.com/), that the application sends log data via the [Loguru](https://github.com/Delgan/loguru) library and sends it to [Grafana Loki](https://grafana.com/oss/loki/).

## ✨ Technology stack

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Nix devenv](https://devenv.sh/)
- [Grafana](https://grafana.com/)
- [SQLite](https://sqlite.org/)
- [Docker](https://www.docker.com/)
- [Github actions](https://github.com/features/actions)
- [AWS Simple Email Service](https://aws.amazon.com/ses/)


## 🎉 Getting started

### ✅ Prerequisites

In order to build & run the app, make sure you have installed [Python 3.11](https://www.python.org/downloads/release/python-3110/).

> If you are using Nix or NixOS you can install it in flake.nix via *devenv*

### 🌱 Setup

1. Add your secrets in `.env` file.

```bash
PORTFOLIO_FROM_EMAIL=john.doe@mail.com
PORTFOLIO_TO_EMAIL=jane.doe@mail.com
PORTFOLIO_EMAIL_HOST="smtp.outlook.com"
PORTFOLIO_EMAIL_USER=user123
PORTFOLIO_EMAIL_PASSWORD=password123
PORTFOLIO_HOST=localhost
PORTFOLIO_ENV=dev
PORTFOLIO_SECRET_KEY="django-insecure-123"
PORTFOLIO_LOKI_URL="https://{{USER}}:{{PASSWORD}}@grafana.net/loki/api/v1/push"
```

2. Install your dependencies

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you're using uv
```bash
uv venv
uv sync
```

### 🏃 Run

```sh
python3 src/manage.py runserver
# Or
make run
```

##  🧑‍💻 Make commands

|Command|Description|
|:-|:-|
|make help|Show available commands with their description|
|make all|Perform check clean test run at the same time|
|make run|Run Django app|
|make test|Test Django app|
|make check|Check the django templates|
|make type-inference|Perform static type check with Pyre|
|make schema-update|Update SQL schema & create an empty migration|
|make sql-init-test|Perform SQL migration|
|make sql-reset|Perform SQL reset|


### 📃 License
This product is licensed under [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html)

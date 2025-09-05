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
The application is hosted on a Raspberry pi 4B in Docker. You can find it's configuration [here](https://github.com/IliyanKostov9/raspberry-pi-dotfiles/blob/master/docker/personal/docker-compose.yaml)

## 🎉 Getting started

### ✅ Prerequisites

In order to build & run the app, make sure you have installed [Python 3.11](https://www.python.org/downloads/release/python-3110/).

> If you are using Nix or NixOS you can install it in flake.nix via *devenv*

### 🌱 Setup

1. Add your secrets in `.env` file.

```bash
FROM_EMAIL = "john.doe@mail.com"
TO_EMAIL = "john.doe@mail.com"
EMAIL_HOST = "smtp.gmail.com" # or whatever you use
EMAIL_USER = "user"
EMAIL_PASSWORD = "password"
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

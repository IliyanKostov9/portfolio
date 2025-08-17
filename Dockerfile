FROM alpine:3.22
ARG DOCKER_USER=portfolio
RUN addgroup -s ${DOCKER_USER} && adduser -S ${DOCKER_USER} -G ${DOCKER_USER}


FROM python:3.11-alpine3.22 AS build
COPY requirements.txt /portfolio/requirements.txt
WORKDIR /portfolio

RUN apk add --no-cache \
	build-base \
	python3-dev \
	musl-dev \
	libffi-dev \
	openssl-dev \
	bash \
	linux-headers

RUN python3 -m venv /opt/.venv \
	&& /opt/.venv/bin/pip install --upgrade pip setuptools wheel \
	&& /opt/.venv/bin/pip install -r requirements.txt

LABEL org.opencontainers.image.source=https://github.com/IliyanKostov9/portfolio \
	version="1.0.0-RELEASE" \
	description="Portfolio app" \
	author="Iliyan Kostov" \
	env="prod"


FROM python:3.11-bookworm
USER ${DOCKER_USER}
WORKDIR /app

COPY --from=build /opt/.venv /app/.venv
COPY --chown=${DOCKER_USER}:${DOCKER_USER} src /app/src


ENV PYTHONPATH=/app:/app/src/apps:/app/src

RUN mkdir -p /var/www/portfolio.ikostov.org/static && \
	/app/.venv/bin/python3 src/manage.py collectstatic

EXPOSE 8000
CMD ["/app/.venv/bin/python3", "-m", "gunicorn", "src.portfolio.asgi:application", "-k", "uvicorn_worker.UvicornWorker", "-b", "0.0.0.0:8000"]

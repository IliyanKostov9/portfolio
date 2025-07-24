FROM alpine:3.22
ARG DOCKER_USER=portfolio
RUN addgroup -s ${DOCKER_USER} && adduser -S ${DOCKER_USER} -G ${DOCKER_USER}


FROM python:3.11 AS build
COPY requirements.txt /portfolio/requirements.txt
WORKDIR /portfolio

RUN python3 -m venv .venv && \
	source .venv/bin/activate && \
	pip install -r requirements.txt

LABEL org.opencontainers.image.source=https://github.com/IliyanKostov9/portfolio \
	version="1.0.0-RELEASE" \
	description="Portfolio app for me" \
	author="Iliyan Kostov" \
	env="prod"


FROM python:3.11
USER ${DOCKER_USER}
WORKDIR /app/

COPY --from=build /portfolio/.venv /app/.venv
COPY --chown=${DOCKER_USER}:${DOCKER_USER} src /app/src

EXPOSE 8080
CMD ["python3", "src/manage.py ", "runserver"]

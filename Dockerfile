FROM alpine:3.22
ARG DOCKER_USER=portfolio
RUN addgroup -s ${DOCKER_USER} && adduser -S ${DOCKER_USER} -G ${DOCKER_USER}

FROM python:3.11 AS build
COPY pyproject.toml /portfolio/pyproject.toml
COPY uv.lock /portfolio/uv.lock
WORKDIR /portfolio

RUN apt-get update && apt-get install -y \
	libsass1 \
	libsass-dev \
	g++ \
	&& rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/.venv \
	&& /opt/.venv/bin/pip install --upgrade pip setuptools wheel uv==0.8.13
# dotenv django_test_migrations django_migration_linter

RUN mkdir /wheels \
	&& SYSTEM_SASS=1 /opt/.venv/bin/pip wheel --no-cache-dir --no-deps --wheel-dir=/wheels libsass

RUN /opt/.venv/bin/pip install --no-cache-dir --find-links=/wheels libsass \
	&& /opt/.venv/bin/uv pip compile pyproject.toml -o requirements.txt \
	&& /opt/.venv/bin/pip install --no-cache-dir -r requirements.txt \
	&& /opt/.venv/bin/pip uninstall -y uv

LABEL org.opencontainers.image.source=https://github.com/IliyanKostov9/portfolio \
	version="1.0.0-RELEASE" \
	description="Portfolio app" \
	author="Iliyan Kostov" \
	env="prod"


FROM python:3.11-bookworm
USER ${DOCKER_USER}
WORKDIR /app

RUN apt-get update && apt-get install -y \
	libsass1 \
	&& rm -rf /var/lib/apt/lists/*

COPY --from=build /opt/.venv /app/.venv
COPY --chown=${DOCKER_USER}:${DOCKER_USER} src /app/src


ENV PYTHONPATH=/app:/app/src/apps:/app/src
ENV PORTFOLIO_ENV="prod"
ENV PORTFOLIO_SKIP_SECRET_KEY_CHECK=true

RUN mkdir -p /var/www/portfolio.ikostov.org/static && \
	/app/.venv/bin/python3 src/manage.py migrate --noinput && \
	/app/.venv/bin/python3 src/manage.py collectstatic --noinput && \
	/app/.venv/bin/python3 src/manage.py compress --force

EXPOSE 8000
CMD ["/app/.venv/bin/python3", "-m", "uvicorn", "src.portfolio.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]

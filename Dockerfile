FROM python:3.10-alpine as base

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as build

ARG PIP_DEFAULT_TIMEOUT=100
ARG PIP_NO_CACHE_DIR=1
ARG POETRY_VERSION=1.3.2

RUN apk add --no-cache gcc libffi-dev musl-dev postgresql-dev
RUN pip install "poetry==${POETRY_VERSION}"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock README.md ./
RUN poetry export -f requirements.txt --without dev | /venv/bin/pip install -r /dev/stdin

ADD kori /app/kori
RUN poetry build && /venv/bin/pip install dist/*.whl

FROM base as final
LABEL org.opencontainers.image.source=https://github.com/madLads-2k19/Kori-Backend

RUN apk add --no-cache libffi libpq
COPY --from=build /venv /venv

CMD . /venv/bin/activate && exec python -m kori

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

ARG PACKAGR_REPOSITORY_URL
ARG PACKAGR_USERNAME
ARG PACKAGR_TOKEN

RUN poetry config repositories.packagr PACKAGR_REPOSITORY_URL && \
    poetry config http-basic.packagr PACKAGR_USERNAME PACKAGR_TOKEN

RUN poetry --version

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main

COPY . .

EXPOSE 8000

ENTRYPOINT ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]


FROM python:3.11.9-slim-bookworm

WORKDIR /opt/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN sudo apt-get update && apt-get install --no-install-recommends -y libpq5

COPY ./dockerization/backend/scripts/run.sh dockerization/backend/scripts/run.sh
COPY ./dockerization/scripts/wait_postgres.sh dockerization/scripts/wait_postgres.sh

COPY django_app/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

COPY ./django_app/ .
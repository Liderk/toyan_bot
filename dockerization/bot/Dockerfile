FROM python:3.11.9-slim-bookworm

WORKDIR /opt/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install --no-install-recommends -y libpq5

COPY ./dockerization/bot/scripts/run.sh dockerization/bot/scripts/run.sh
COPY ./dockerization/scripts/wait_postgres.sh dockerization/scripts/wait_postgres.sh

COPY telegram_app/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./telegram_app/ telegram_app/

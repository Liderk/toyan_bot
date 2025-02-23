FROM python:3.11.9-slim-bookworm

WORKDIR /opt/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY dockerization/bot/scripts/run.sh dockerization/bot/scripts/run.sh
COPY dockerization/scripts/run.sh dockerization/scripts/run.sh

COPY telegram_app/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./telegram_app/ .

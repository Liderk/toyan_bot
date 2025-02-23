FROM python:3.11.9-slim-bookworm

WORKDIR /opt/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY django_app/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

WORKDIR /opt/app/django_app

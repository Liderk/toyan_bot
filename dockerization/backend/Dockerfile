FROM python:3.11.9-slim-bookworm

WORKDIR /opt/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install --no-install-recommends -y libpq5 curl

COPY django_app/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./django_app/ .
COPY --chmod=777 ./dockerization/backend/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["docker-entrypoint.sh"]
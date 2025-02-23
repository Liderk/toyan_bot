#!/usr/bin/env sh

set -e

chown www-data:www-data /var/log
python manage.py collectstatic --noinput
sleep 5
python manage.py migrate
gunicorn config.wsgi --bind 0.0.0.0:5000

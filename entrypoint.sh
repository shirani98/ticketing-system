#!/bin/bash
set -e

python manage.py migrate --noinput

if [ "$#" -gt 0 ]; then
  exec "$@"
fi

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2

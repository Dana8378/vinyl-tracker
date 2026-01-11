#!/usr/bin/env bash

pip install -r requirements.txt

python manage.py collectstatic --noinput

if [ -n "$DATABASE_URL" ]; then
    python manage.py migrate
fi
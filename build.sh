#!/usr/bin/env bash

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py seed_data

if [ -n "$DATABASE_URL" ]; then
    python manage.py migrate
fi
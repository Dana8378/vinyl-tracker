#!/usr/bin/env bash

echo "=== Установка зависимостей ==="
pip install -r requirements.txt

echo "=== Применение миграций ==="
python manage.py migrate

echo "=== Сбор статических файлов ==="
python manage.py collectstatic --noinput

echo "=== Сборка завершена ==="
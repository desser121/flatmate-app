#!/bin/sh
set -ex

echo "=== ENV CHECK ==="
echo "PORT=$PORT"
echo "DATABASE_URL=${DATABASE_URL:+SET}"
echo "DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-NOT SET}"
echo "SECRET_KEY=${SECRET_KEY:+SET}"

echo "=== MIGRATIONS ==="
python manage.py migrate --noinput

echo "=== TEST WSGI ==="
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
import django
django.setup()
from django.test.utils import setup_test_environment
print('Django setup OK')
"

echo "=== START GUNICORN ==="
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120 \
    --log-level debug \
    --access-logfile - \
    --error-logfile -

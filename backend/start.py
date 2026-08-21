#!/usr/bin/env python
"""Railway startup script."""
import os
import sys
import subprocess

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

print(f"PORT={os.environ.get('PORT', 'EMPTY')}")
print(f"DATABASE_URL={'SET' if os.environ.get('DATABASE_URL') else 'EMPTY'}")
print(f"DJANGO_SETTINGS_MODULE={os.environ['DJANGO_SETTINGS_MODULE']}")

print("Running migrations...")
sys.stdout.flush()
result = subprocess.run([sys.executable, 'manage.py', 'migrate', '--noinput'])
if result.returncode != 0:
    print(f"Migrations failed: {result.returncode}")
    sys.exit(1)

print("Migrations done. Testing WSGI import...")
sys.stdout.flush()

try:
    from config.wsgi import application
    print("WSGI import OK")
except Exception as e:
    print(f"WSGI import FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Starting gunicorn...")
sys.stdout.flush()
os.execvp('gunicorn', ['gunicorn', 'config.wsgi:application', '--bind', f'0.0.0.0:{os.environ.get("PORT", "8000")}', '--timeout', '120', '--access-logfile', '-', '--error-logfile', '-'])

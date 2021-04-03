release: . venv/bin/activate ; venv/bin/python manage.py makemigrations ; venv/bin/python manage.py migrate ; ls /tmp ;touch /tmp/app-initialized
web: bin/start-nginx venv/bin/gunicorn onlinechess.asgi:application -b=unix:/tmp/nginx.socket -k uvicorn.workers.UvicornWorker

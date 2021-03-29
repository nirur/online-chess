release: . venv/bin/activate ; venv/bin/python manage.py makemigrations ; venv/bin/python manage.py migrate
web: bin/start-nginx bundle exec "venv/bin/gunicorn onlinechess.asgi:application -b=unix:///tmp/nginx.socket -k uvicorn.workers.UvicornWorker & touch /tmp/app-initialized"

release: . venv/bin/activate ; venv/bin/python manage.py makemigrations ; venv/bin/python manage.py migrate ; touch /tmp/app-initialized
web: bin/start-nginx "venv/bin/gunicorn onlinechess.asgi:application -b=0.0.0.0:$PORT -k uvicorn.workers.UvicornWorker ; ls /tmp"

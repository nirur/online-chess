release: . venv/bin/activate ; venv/bin/python manage.py makemigrations ; venv/bin/python manage.py migrate
web: venv/bin/gunicorn -bind=0.0.0.0:$PORT 'onlinechess.asgi:application' -k uvicorn.workers.UvicornWorker

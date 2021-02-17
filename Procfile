web: source venv/bin/activate ; venv/bin/python3 manage.py runserver 0.0.0.0:$PORT ; venv/bin/gunicorn onlinechess.asgi:application -k uvicorn.workers.UvicornWorker

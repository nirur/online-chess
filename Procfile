release: . venv/bin/activate ; venv/bin/python manage.py makemigrations ; venv/bin/python manage.py migrate
web: venv/bin/daphne onlinechess.asgi:application --port $PORT --bind 0.0.0.0
worker: venv/bin/python manage.py runworker channel_layer

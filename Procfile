release: . venv/bin/activate ; venv/bin/python manage.py makemigrations ; venv/bin/python manage.py migrate ; export DJANGO_SUPERUSER_PASSWORD="NadminR2020" ; venv/bin/python manage.py createsuperuser --noinput --username NiraoAdmin641
web: venv/bin/gunicorn onlinechess.asgi:application -b=0.0.0.0:$PORT -k uvicorn.workers.UvicornWorker

release: source venv/bin/activate ; \
         venv/bin/python manage.py makemigrations ; \
         echo "from django.contrib.auth.models import User; User.objects.create_superuser('NiraoAdmin641', password='NadminR2020')" | python3 manage.py shell
web: venv/bin/gunicorn onlinechess.asgi:application -b=0.0.0.0:$PORT -k uvicorn.workers.UvicornWorker

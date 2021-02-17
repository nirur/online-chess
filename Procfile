release: source /app/venv/bin/activate ; /app/venv/bin/python manage.py makemigrations ; echo "from django.contrib.auth.models import User; User.objects.create_superuser('NiraoAdmin641', password='$PSWD')" | /app/venv/bin/python manage.py shell
web: venv/bin/gunicorn onlinechess.asgi:application -b=0.0.0.0:$PORT -k uvicorn.workers.UvicornWorker

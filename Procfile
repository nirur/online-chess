release: source /app/venv/bin/activate ; which python ;python manage.py makemigrations ; echo "from django.contrib.auth.models import User; User.objects.create_superuser('NiraoAdmin641', password='$PSWD', last_login='$(date)')" | python manage.py shell
web: gunicorn onlinechess.asgi:application -b=0.0.0.0:$PORT -k uvicorn.workers.UvicornWorker

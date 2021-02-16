venv/bin/python manage.py collectstatic --no-input

sudo /etc/init.d/nginx restart

venv/bin/redis-stable/src/redis-server & venv/bin/python manage.py runserver localhost:8001

venv/bin/python3 manage.py collectstatic --no-input

#sudo /etc/init.d/nginx restart

venv/bin/redis-stable/src/redis-server & venv/bin/python3 manage.py runserver 192.168.86.30:8001

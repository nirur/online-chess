python3 manage.py collectstatic --no-input
python3 manage.py compilestatic
sudo /etc/init.d/nginx restart
venv/bin/redis-stable/src/redis-server & daphne onlinechess.asgi:application -b=192.168.86.30 -p=8001 --proxy-headers

"""
ASGI config for onlinechess project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os, sys

import django
from django.core.asgi import get_asgi_application

sys.path.append('/home/django-projects/onlinechess-project/')
sys.path.append('/home/django-projects/onlinechess-project/venv/lib/python3.8/site-packages')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinechess.settings')

os.environ['channels_users'] = ''

django.setup()

print(dict(os.environ).keys())
print(('DATABASE_URL' in dict(os.environ).keys()))

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from onlinechess.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
                      'http':get_asgi_application(),
                      'websocket':AuthMiddlewareStack(
                          URLRouter(websocket_urlpatterns)
                          )
                      })


"""
WSGI config for onlinechess project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('/home/django-projects/onlinechess-project/')
sys.path.append('/home/django-projects/onlinechess-project/venv/lib/python3.8/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onlinechess.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

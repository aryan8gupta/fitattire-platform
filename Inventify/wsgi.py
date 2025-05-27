"""
WSGI config for Inventify project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import Inventify


settings_module = 'Inventify.deployment' if 'https://inventory-management-app-hnbvgqaag3g2hyde.centralindia-01.azurewebsites.net/' in os.environ else 'Inventify.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', Inventify.deployment)

application = get_wsgi_application()

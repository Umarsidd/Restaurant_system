"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Debug: Check environment variable
django_env = os.environ.get('DJANGO_ENV', 'not-set')
settings_module = 'config.production_settings' if django_env == 'production' else 'config.settings'
print(f"🔍 DJANGO_ENV={django_env}, Using settings: {settings_module}")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()

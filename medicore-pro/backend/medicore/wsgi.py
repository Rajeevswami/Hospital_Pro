"""WSGI config for MediCore Pro."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicore.settings.development')
application = get_wsgi_application()

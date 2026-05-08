"""Development settings."""
from .base import *  # noqa: F401,F403

DEBUG = True
ALLOWED_HOSTS = ['*']

# Use console email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Enable browsable API renderer in dev
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (  # noqa: F405
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)

CORS_ALLOW_ALL_ORIGINS = True
INTERNAL_IPS = ['127.0.0.1']

"""Production settings with hardened security."""
from .base import *  # noqa: F401,F403
import sentry_sdk

DEBUG = False

# ── Security Headers ──
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ── Sentry ──
sentry_sdk.init(
    dsn=env('SENTRY_DSN', default=''),  # noqa: F405
    traces_sample_rate=0.2,
    profiles_sample_rate=0.1,
)

# ── Email (SES / SMTP) ──
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='')  # noqa: F405
EMAIL_PORT = env.int('EMAIL_PORT', default=587)  # noqa: F405
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')  # noqa: F405
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')  # noqa: F405
DEFAULT_FROM_EMAIL = 'MediCore Pro <noreply@medicorepro.com>'

# ── Static Files ──
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ── Logging ──
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '{levelname} {asctime} {module} {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'},
    },
    'root': {'handlers': ['console'], 'level': 'WARNING'},
    'loggers': {
        'apps': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
    },
}

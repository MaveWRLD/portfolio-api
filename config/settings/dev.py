from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

CSRF_TRUSTED_ORIGINS = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += ["silk"]
MIDDLEWARE = ["silk.middleware.SilkyMiddleware"] + MIDDLEWARE

SILKY_PYTHON_PROFILER = True

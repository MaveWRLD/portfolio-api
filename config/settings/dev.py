from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

CSRF_TRUSTED_ORIGINS = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# debug_toolbar disabled locally: its SQL/Templates panels import
# django.contrib.gis.gdal, which isn't installed in this env and makes every
# server start slow (or fail) trying to locate a GDAL library.
# INSTALLED_APPS += ["debug_toolbar"]
# MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
#
# INTERNAL_IPS = ["127.0.0.1"]
#
# DEBUG_TOOLBAR_CONFIG = {
#     "SHOW_TOOLBAR_CALLBACK": lambda request: True,
# }

# MinIO uses self-signed certs, disable SSL verification for local dev
AWS_S3_VERIFY = False
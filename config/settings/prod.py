import os

from .base import *

DEBUG = False

# Temporary, opt-in only. Set ENABLE_SILK=true on Render to profile requests
# in prod-like conditions, then unset it and redeploy when done. Records
# full request/response bodies + SQL + call graph in its own DB tables and
# UI at /silk/ — unlike debug_toolbar it works on JSON responses too.
# Gated behind a real login (staff account), not IP/cookie tricks, since
# silk ships that natively and Render's proxy hides the real client IP.
if os.getenv("ENABLE_SILK", "false").lower() == "true":
    INSTALLED_APPS += ["silk"]
    MIDDLEWARE = ["silk.middleware.SilkyMiddleware"] + MIDDLEWARE

    # Left off: gunicorn runs gthread workers here, and cProfile's per-thread
    # enable() collides across concurrent threads on the same worker
    # ("Another profiling tool is already active"). SQL/request logging
    # below doesn't need it — enable locally (sync/single-thread) if you
    # need the call graph.
    SILKY_AUTHENTICATION = True
    SILKY_AUTHORISATION = True
    SILKY_PERMISSIONS = lambda user: user.is_staff  # noqa: E731

    LOGIN_URL = f"/{ADMIN_URL}login/"

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
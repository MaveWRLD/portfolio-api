import os

from .base import *

DEBUG = False

# Temporary, opt-in only. Set ENABLE_DEBUG_TOOLBAR=true and DEBUG_TOOLBAR_KEY
# on Render to inspect a request in prod-like conditions, then unset both and
# redeploy when done. Render sits behind a proxy so REMOTE_ADDR is the LB's
# IP, not the caller's — gate on a shared secret cookie instead of IP.
# Set the cookie once via the browser console:
#   document.cookie = "dbg=<DEBUG_TOOLBAR_KEY value>; path=/"
if os.getenv("ENABLE_DEBUG_TOOLBAR", "false").lower() == "true":
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

    _toolbar_key = os.getenv("DEBUG_TOOLBAR_KEY", "")

    def _show_toolbar(request):
        return bool(_toolbar_key) and request.COOKIES.get("dbg") == _toolbar_key

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": _show_toolbar,
    }

    # ProfilingPanel is off by default — it's the one that shows a call
    # graph (which function actually ate the time), not just SQL vs. total.
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.history.HistoryPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ]

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
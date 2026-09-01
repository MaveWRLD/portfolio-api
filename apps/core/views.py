from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    db_ok = False
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_ok = True
    except Exception:
        pass

    return Response(
        {
            "status": "healthy" if db_ok else "degraded",
            "database": "connected" if db_ok else "disconnected",
        },
        status=200 if db_ok else 503,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def readiness_check(request):
    return Response({"status": "ready"}, status=200)
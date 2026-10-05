from django.db import DatabaseError, connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def healthz(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except DatabaseError:
        return JsonResponse({"status": "error", "db": "error"}, status=503)
    return JsonResponse({"status": "ok", "db": "ok"})

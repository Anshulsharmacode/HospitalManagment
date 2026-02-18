from django.http import JsonResponse


def success_response(data=None, message="Success", status=200):
    payload = {
        "success": True,
        "message": message,
    }
    if data is not None:
        payload["data"] = data
    return JsonResponse(payload, status=status)


def error_response(message="Something went wrong", status=400, errors=None):
    payload = {
        "success": False,
        "message": message,
    }
    if errors is not None:
        payload["errors"] = errors
    return JsonResponse(payload, status=status)

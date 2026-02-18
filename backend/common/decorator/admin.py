from functools import wraps
from backend.apps.users.models import UserRole
from common.api.api import error_response, success_response


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return error_response("Authentication required", status=401)

        if request.user.role != UserRole.ADMIN:
            return error_response("Admin access required", status=403)

        return view_func(request, *args, **kwargs)

    return wrapper
import json

from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

from backend.common.decorator.admin import admin_required
from common.api.api import error_response, success_response

from .models import AuthToken, User, UserRole


def _parse_json(request):
    try:
        return json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None



def signup_view(request):
    if request.method != "POST":
        return error_response(message="Method not allowed", status=405)

    payload = _parse_json(request)
    if payload is None:
        return error_response(message="Invalid JSON payload", status=400)

    email = str(payload.get("email", "")).strip().lower()
    password = payload.get("password")
    role = UserRole.PATIENT
    name = str(payload.get("Name", "")).strip()
    phoneNumber = payload.get('phoneNumber')
    # last_name = str(payload.get("last_name", "")).strip()

    if not email or not password:
        return error_response(message="email and password are required", status=400)

    if role not in UserRole.values:
        return error_response(message="Invalid role", status=400)

    if User.objects.filter(email=email).exists():
        return error_response(message="Email already registered", status=400)

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        role=role,
        name=name,
        phoneNumber=phoneNumber
    )
    return success_response(
        data={
            "id": user.id,
            "email": user.email,
            "role": user.role,
        },
        message="Signup successful",
        status=201,
    )



def signin_view(request):
    if request.method != "POST":
        return error_response(message="Method not allowed", status=405)

    payload = _parse_json(request)
    if payload is None:
        return error_response(message="Invalid JSON payload", status=400)

    email = str(payload.get("email", "")).strip().lower()
    password = payload.get("password")

    if not email or not password:
        return error_response(message="email and password are required", status=400)

    user = authenticate(request, email=email, password=password)
    if user is None:
        return error_response(message="Invalid credentials", status=401)

    login(request, user)
    token = AuthToken.objects.create(user=user)
    return success_response(
        data={
            "token": token.key,
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
            },
        },
        message="Signin successful",
        status=200,
    )


@admin_required
def create_staff(request):
    if request.method != 'POST':
        return error_response(message="Method not allowed", status=405)

    payload = _parse_json(request)
    if payload is None:
        return error_response(message="Invalid JSON payload", status=400)

    email = str(payload.get("email", "")).strip().lower()

    password = payload.get('password')
    username= payload.get('username')
    role = payload.get('role')
    phoneNumber = payload.get('phoneNumber')
    name = str(payload.get("Name", "")).strip()

    if not email or not password:
        return error_response(message="email and password are required", status=400)

    if role not in UserRole.values:
        return error_response(message="Invalid role", status=400)

    if User.objects.filter(email=email).exists():
        return error_response(message="Email already registered", status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        role=role,
        name=name,
        phoneNumber=phoneNumber
    )

    return success_response(
        data={
            "id": user.id,
            "email": user.email,
            "role": user.role,
        },
        message="Staff created successfully",
        status=201,
    )

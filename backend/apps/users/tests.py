from django.test import TestCase
from django.urls import reverse

from .models import AuthToken, User, UserRole


class AuthenticationApiTests(TestCase):
    def test_signup_creates_user(self):
        response = self.client.post(
            reverse("signup"),
            data={
                "email": "doctor1@hospital.com",
                "password": "StrongPass123!",
                "role": UserRole.DOCTOR,
                "first_name": "Asha",
                "last_name": "Khan",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        user = User.objects.get(email="doctor1@hospital.com")
        self.assertEqual(user.role, UserRole.DOCTOR)
        self.assertTrue(user.check_password("StrongPass123!"))

    def test_signup_rejects_duplicate_email(self):
        User.objects.create_user(
            username="admin@hospital.com",
            email="admin@hospital.com",
            password="Admin123!",
            role=UserRole.ADMIN,
        )

        response = self.client.post(
            reverse("signup"),
            data={
                "email": "admin@hospital.com",
                "password": "Another123!",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Email already registered")

    def test_signin_returns_token_for_valid_credentials(self):
        user = User.objects.create_user(
            username="reception@hospital.com",
            email="reception@hospital.com",
            password="Recep123!",
            role=UserRole.RECEPTION,
        )

        response = self.client.post(
            reverse("signin"),
            data={"email": user.email, "password": "Recep123!"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())
        self.assertEqual(AuthToken.objects.filter(user=user).count(), 1)

    def test_signin_rejects_invalid_credentials(self):
        User.objects.create_user(
            username="tech@hospital.com",
            email="tech@hospital.com",
            password="TechPass123!",
            role=UserRole.TECHNICIAN,
        )

        response = self.client.post(
            reverse("signin"),
            data={"email": "tech@hospital.com", "password": "WrongPass"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "Invalid credentials")

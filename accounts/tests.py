from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "TestPassword123"

        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

    def test_register_user(self):
        response = self.client.post(
            "/register/",
            {
                "username": "newuser",
                "password": "NewPassword123"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertIn("access_token", response.data)

        self.assertTrue(
            User.objects.filter(username="newuser").exists()
        )

    def test_register_duplicate_username(self):
        response = self.client.post(
            "/register/",
            {
                "username": self.username,
                "password": "AnotherPassword123"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_register_without_username(self):
        response = self.client.post(
            "/register/",
            {
                "password": "TestPassword123"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_register_without_password(self):
        response = self.client.post(
            "/register/",
            {
                "username": "newuser"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_login(self):
        response = self.client.post(
            "/login/",
            {
                "username": self.username,
                "password": self.password
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_password(self):
        response = self.client.post(
            "/login/",
            {
                "username": self.username,
                "password": "WrongPassword"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
    def test_logout(self):
        login_response = self.client.post(
            "/login/",
            {
                "username": self.username,
                "password": self.password
            },
            format="json"
        )

        access_token = login_response.data["access"]
        refresh_token = login_response.data["refresh"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = self.client.post(
            "/logout/",
            {
                "refresh": refresh_token
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["message"],
            "Logout successful"
        )

    def test_logout_without_authentication(self):
        response = self.client.post(
            "/logout/",
            {
                "refresh": "some-refresh-token"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_logout_without_refresh_token(self):
        login_response = self.client.post(
            "/login/",
            {
                "username": self.username,
                "password": self.password
            },
            format="json"
        )

        access_token = login_response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = self.client.post(
            "/logout/",
            {},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )



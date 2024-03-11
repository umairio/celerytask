from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile, User
from .serializers import ProfileSerializer


class MainAppTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.test", password="testpass"
        )
        self.profile = Profile.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.email, "test@test.test")

    def test_profile_creation(self):
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(self.profile.user, self.user)

    def test_login(self):
        response = self.client.post(
            "/api/login/", {"email": "test@test.test", "password": "testpass"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscription_update(self):
        # First request with a future date should return 200
        response = self.client.patch(
            "/api/subscription/",
            {"subscription_start_date": str(datetime.now())},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Second request with a past date should return 400
        response = self.client.patch(
            "/api/subscription/",
            {"subscription_start_date": "2020-03-09 09:34:00"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"],
            "start date cannot be older than current time.",
        )

    def test_logout(self):
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post("/api/logout/", {"refresh": str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_serializer(self):
        new_user = User.objects.create_user(
            email="newuser@test.test", password="newuserpass"
        )

        data = {
            "user": new_user.id,
            "subscription_start_date": str(datetime.now()),
            "subscription_end_date": str(datetime.now() + timedelta(hours=1)),
        }
        serializer = ProfileSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

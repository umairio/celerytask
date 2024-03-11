from django.utils.timezone import now, timedelta
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
        future_date = (now() + timedelta(minutes=20)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        response = self.client.patch(
            "/api/subscription/",
            {"subscription_start_date": future_date},
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

        past_date = (now() - timedelta(minutes=20)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        response = self.client.patch(
            "/api/subscription/",
            {"subscription_start_date": past_date},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout(self):
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post("/api/logout/", {"refresh": str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_serializer(self):
        new_user = User.objects.create_user(
            email="newuser@test.test", password="newuserpass"
        )

        future_date = (now() + timedelta(minutes=20)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        data = {
            "user": new_user.id,
            "subscription_start_date": future_date,
        }
        serializer = ProfileSerializer(data=data)
        self.assertTrue(serializer.is_valid())

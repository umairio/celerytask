from datetime import datetime, timedelta

from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    def post(self, request):
        refresh = request.data.get("refresh")

        if not refresh:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh)
            token.blacklist()
            return Response(
                {"message": "Logout successful."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SubscriptionUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        profile = request.user.profile
        sub_start_date = request.data.get("subscription_start_date")
        try:
            sub_start_date = datetime.strptime(sub_start_date,
                                               "%Y-%m-%d %H:%M:%S")
        except ValueError:
            sub_start_date = datetime.strptime(sub_start_date,
                                               "%Y-%m-%d %H:%M:%S.%f")
        sub_start_date = timezone.make_aware(sub_start_date)
        tenminearly = timezone.now() - timedelta(minutes=10)
        if sub_start_date > tenminearly:
            profile.subscription_start_date = sub_start_date
            profile.subscription_end_date = (
                profile.subscription_start_date + timedelta(
                    hours=1
                )
            )
            profile.save()
            return Response(
                {"message": "Subscription updated successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "start date cannot be older than current time."},
                status=status.HTTP_400_BAD_REQUEST,
            )


def index(request):
    # populate_users_profiles.delay()
    return render(request, "index.html")

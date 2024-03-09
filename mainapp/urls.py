from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import LogoutView, RegisterView, SubscriptionUpdateView, index

router = routers.DefaultRouter()


urlpatterns = [
    path("", index),
    path("api/", include(router.urls)),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/login/refresh/", TokenRefreshView.as_view()),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("api/subscription/", SubscriptionUpdateView.as_view()),
]

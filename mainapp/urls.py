from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework import routers


router = routers.DefaultRouter()


urlpatterns = [
    path('', index),
    path("api/", include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/subscription/', SubscriptionUpdateView.as_view(), name='subscription'),
]
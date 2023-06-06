from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView,
)

from user.views import RegisterView, UserActivityView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="create"),
    path("login/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("ligin/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("login/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("activity/", UserActivityView.as_view(), name="user-activity"),
]

app_name = "user"

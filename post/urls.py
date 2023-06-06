from django.urls import path, include
from rest_framework import routers

from post.views import PostViewSet, AnalyticsViewSet

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("analytics", AnalyticsViewSet, basename="analytics")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "post"

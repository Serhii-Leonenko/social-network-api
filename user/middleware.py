from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication


class UpdateLastRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authentication = JWTAuthentication()

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            user = get_user_model().objects.get(username=request.user)
            user.last_request_time = timezone.now()
            user.save()

        return response

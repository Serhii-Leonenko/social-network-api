from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from user.serializers import UserSerializer, UserActivitySerializer

User = get_user_model()


class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            },
            status=status.HTTP_201_CREATED,
        )


class UserActivityView(APIView):
    serializer_class = UserActivitySerializer

    def get(self, request):
        serializer = self.serializer_class(instance=request.user)

        return Response(serializer.data)

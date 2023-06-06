from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "password", "first_name", "last_name")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        return user


class UserActivitySerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    last_request_time = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ("last_login", "last_request_time")

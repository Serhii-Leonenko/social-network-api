from rest_framework import serializers

from post.models import Post, Like
from user.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "user", "title", "content", "created_at", "updated_at", "likes_count")
        read_only_fields = ("user", "created_at", "updated_at")

    @staticmethod
    def get_likes_count(obj):
        return obj.likes.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "user", "post", "created_at")


class PostDetailSerializer(PostSerializer):
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "user", "content", "created_at", "updated_at", "likes")
        read_only_fields = ("user", "created_at", "updated_at")

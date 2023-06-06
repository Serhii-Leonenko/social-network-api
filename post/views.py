from django.db.models import Count
from django.utils.dateparse import parse_date
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from post.models import Post, Like
from post.permissions import IsAuthor
from post.serializers import PostSerializer, PostDetailSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthor]

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.query_params.get("user")

        if user:
            self.queryset = self.queryset.filter(user=user)

        return self.queryset

    def get_serializer_class(self):
        if self.action in ["like_unlike", "retrieve"]:
            return PostDetailSerializer

        return self.serializer_class

    @action(detail=True, methods=["post"])
    def like_unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if post.likes.filter(user=user).exists():
            post.likes.filter(user=user).delete()
            message = "Post unliked"
        else:
            Like.objects.create(user=user, post=post)
            message = "Post liked"

        serializer = self.get_serializer(post)

        return Response({"message": message, "post": serializer.data})


class AnalyticsViewSet(viewsets.ViewSet):
    def list(self, request):
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        if not date_from or not date_to:
            return Response({"message": "Please provide date_from and date_to"})

        likes_analytics = (
            Like.objects.filter(
                created_at__date__gte=parse_date(date_from),
                created_at__date__lte=parse_date(date_to),
            )
            .values("created_at__date")
            .annotate(total_likes=Count("id"))
        )

        return Response(likes_analytics)

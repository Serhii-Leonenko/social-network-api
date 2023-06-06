from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from post.models import Post
from post.serializers import PostSerializer

POST_URL = reverse("post:post-list")


def create_posts(number: int, user):
    result = []

    for i in range(number):
        result.append(
            Post.objects.create(
                title=f"test_title_{i}", content=f"test_content_{i}", user=user
            )
        )

    return result


class UnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(POST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = get_user_model().objects.create_user("test_user_1", "test_user_1")
        self.user_2 = get_user_model().objects.create_user("test_user_2", "test_user_2")
        self.client.force_authenticate(self.user_1)

    def test_authenticated_list_posts(self):
        create_posts(10, self.user_1)
        create_posts(5, self.user_2)

        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        response = self.client.get(POST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_is_author_required_to_update_the_post(self):
        created_post = create_posts(1, self.user_2)

        response = self.client.put(
            reverse("post:post-detail", args=[created_post[0].id]),
            data={"title": "new_title", "content": "new_content"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

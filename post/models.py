from django.conf import settings
from django.db import models
from rest_framework.exceptions import ValidationError


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        if Post.objects.filter(title=self.title, user=self.user).exists():
            error_message = "A post with the same title already exists for this user."
            raise ValidationError(error_message)

        super().save(*args, **kwargs)


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

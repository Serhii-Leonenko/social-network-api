# Generated by Django 4.2.1 on 2023-06-07 07:00

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("post", "0008_alter_post_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="post",
            unique_together={("title", "user")},
        ),
    ]

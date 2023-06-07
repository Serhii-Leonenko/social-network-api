# Generated by Django 4.2.1 on 2023-06-07 06:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("post", "0006_alter_post_title"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="post",
            unique_together={("title", "user")},
        ),
    ]

# Generated by Django 4.2.1 on 2023-06-06 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0004_alter_like_post"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ("-created_at",)},
        ),
        migrations.AddField(
            model_name="post",
            name="title",
            field=models.CharField(default="", max_length=255),
        ),
    ]

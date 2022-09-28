# Generated by Django 4.1.1 on 2022-09-28 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_alter_recipe_public"),
    ]

    operations = [
        migrations.CreateModel(
            name="FollowRelationship",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "followee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="follows_where_I_am_the_one_being_followed",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "follower",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="follows_where_I_am_the_follower",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

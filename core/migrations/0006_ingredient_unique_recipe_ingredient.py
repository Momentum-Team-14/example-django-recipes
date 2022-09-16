# Generated by Django 4.1.1 on 2022-09-16 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_mealplan_mealplan_unique_user_date"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="ingredient",
            constraint=models.UniqueConstraint(
                fields=("recipe", "item"), name="unique_recipe_ingredient"
            ),
        ),
    ]
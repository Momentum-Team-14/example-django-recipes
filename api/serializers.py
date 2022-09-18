from core.models import Recipe, Ingredient, User
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"
        read_only_fields = ["recipe"]


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    recipe_url = serializers.HyperlinkedIdentityField(view_name="recipe-detail")

    class Meta:
        model = Recipe
        fields = ["pk", "title", "public", "author", "favorited_by", "recipe_url"]


class RecipeDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    original_recipe = serializers.HyperlinkedRelatedField(
        view_name="recipe-detail", read_only=True
    )

    class Meta:
        model = Recipe
        fields = "__all__"


class RecipeCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            "pk",
            "title",
            "prep_time_in_minutes",
            "cook_time_in_minutes",
            "original_recipe",
        ]

    def create(self, validated_data):
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in recipe.original_recipe.ingredients.all():
            new_ingredient = ingredient
            new_ingredient.pk = None
            new_ingredient.recipe = recipe
            new_ingredient.save()
        return recipe


class UserForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "username", "first_name", "last_name", "email", "is_staff"]

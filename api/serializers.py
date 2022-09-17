from core.models import Recipe, Ingredient
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

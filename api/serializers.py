from core.models import Recipe
from rest_framework import serializers

class RecipeSerializer(serializers.ModelSerializer):
  author = serializers.SlugRelatedField(slug_field="username", read_only=True)
  class Meta:
    model=Recipe
    fields="__all__"

from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from .serializers import RecipeSerializer, IngredientSerializer
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from core.models import Recipe, Ingredient


class RecipeListCreateView(ListCreateAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # write a query that gets recipes that were authored by the authenticated user
        # You could do it like this:
        # queryset = Recipe.objects.filter(author=self.request.user)
        # But you can also use the related name from your Recipe model!
        queryset = self.request.user.recipes.all()
        return queryset


class IngredientCreateView(CreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def perform_create(self, serializer):
        # look up the recipe that this ingredient is for
        # make sure the authenticated user who is adding the ingredient actually owns the recipe
        recipe = get_object_or_404(self.request.user.recipes, pk=self.kwargs.get("pk"))
        # save the ingredient with the related recipe
        serializer.save(recipe=recipe)

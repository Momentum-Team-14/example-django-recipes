from django.shortcuts import render, get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .serializers import RecipeSerializer, IngredientSerializer, RecipeDetailSerializer
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import Recipe, Ingredient
from django.db import IntegrityError
from django.db.models import Q


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

        try:
            # save the ingredient with the related recipe
            serializer.save(recipe=recipe)
        except IntegrityError as error:
            # handle the case where the same ingredient already exists
            raise serializers.ValidationError({"error": error})


class RecipeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # return recipe details if the authenticated user is the author of the recipe
        # OR if the recipe is marked as public
        return queryset.filter(Q(author=self.request.user) | Q(public=True))


class RecipeListPublicView(ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return self.queryset.filter(public=True)

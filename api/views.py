from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .serializers import RecipeSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from core.models import Recipe

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

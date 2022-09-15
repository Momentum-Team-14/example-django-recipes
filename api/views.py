from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .serializers import RecipeSerializer
from rest_framework import status
from core.models import Recipe

class RecipeListCreateView(ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer



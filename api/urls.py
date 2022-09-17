from django.urls import path
from rest_framework import routers
from . import views

urlpatterns = [
    path("recipes/", views.RecipeListCreateView.as_view(), name="recipe-list"),
    path(
        "recipes/<int:pk>/ingredients",
        views.IngredientCreateView.as_view(),
        name="new-ingredient",
    ),
]

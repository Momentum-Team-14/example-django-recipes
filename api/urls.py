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
    path(
        "recipes/public",
        views.RecipeListPublicView.as_view(),
        name="recipe-list-public",
    ),
    path("recipes/<int:pk>", views.RecipeDetailView.as_view(), name="recipe-detail"),
    path("recipes/<int:pk>/copy", views.RecipeCopyView.as_view(), name="recipe-copy"),
    path("admin/users", views.UserListAdminView.as_view(), name="user-list"),
    path(
        "mealplan/<int:year>/<int:month>/<int:day>",
        views.MealPlanView.as_view(),
        name="mealplan",
    ),
]

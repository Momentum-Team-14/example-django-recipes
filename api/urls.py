from django.urls import path
from . import views

urlpatterns = [path("", views.RecipeListCreateView.as_view())]

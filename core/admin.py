from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import RecipeStep, User, Recipe, Ingredient, MealPlan, FollowRelationship

admin.site.register(User, UserAdmin)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeStep)
admin.site.register(MealPlan)
admin.site.register(FollowRelationship)

import datetime
from django.shortcuts import render, get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from .serializers import (
    RecipeSerializer,
    IngredientSerializer,
    RecipeDetailSerializer,
    RecipeCopySerializer,
    UserForAdminSerializer,
    MealPlanSerializer,
    UsersIFollowSerializer,
    NewFollowSerializer,
)
from rest_framework.views import APIView
from rest_framework import status, serializers, response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .permissions import IsOwningUser
from core.models import Recipe, Ingredient, User, MealPlan, FollowRelationship
from django.db import IntegrityError
from django.db.models import Q


class SmallResultsSet(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 5


class RecipeListCreateView(ListCreateAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SmallResultsSet

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
    permission_classes = [IsAuthenticated]

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


class UserListAdminView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserForAdminSerializer
    permission_classes = [IsAdminUser]


class RecipeCopyView(CreateAPIView):
    serializer_class = RecipeCopySerializer

    def create(self, request, *args, **kwargs):
        original_recipe = get_object_or_404(Recipe, pk=kwargs.get("pk"))
        serializer = self.get_serializer(
            data={
                "title": original_recipe.title,
                "prep_time_in_minutes": original_recipe.prep_time_in_minutes,
                "cook_time_in_minutes": original_recipe.cook_time_in_minutes,
                "original_recipe": original_recipe.pk,
            }
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, public=False)


class MealPlanView(APIView):
    """
    Return the titles and URLS of recipes for a mealplan on a given date
    """

    permission_classes = [IsAuthenticated, IsOwningUser]

    def get(self, request, format=None, month=None, day=None, year=None):
        mealplan_date = datetime.date(year, month, day)
        mealplan = get_object_or_404(MealPlan, date=mealplan_date)
        self.check_object_permissions(request, mealplan)
        serializer = MealPlanSerializer(mealplan, context={"request": request})
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class RecipePublishView(UpdateAPIView):
    """
    A recipe author can mark a recipe as public to publish it.
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return self.request.user.recipes.all()

    def get_object(self):
        recipe = super().get_object()
        if self.request.user != recipe.author:
            raise PermissionDenied()
            # I don't really need to do this check if have set the queryset
            # to _only_ the recipes belonging to the authenticated user
            # but it makes this extra explicit
        return recipe

    def perform_update(self, serializer):
        serializer.save(public=True)


class FollowListCreateView(ListCreateAPIView):
    serializer_class = UsersIFollowSerializer
    queryset = FollowRelationship.objects.all()

    def get_queryset(self):
        return self.request.user.follows_where_I_am_the_follower.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return NewFollowSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

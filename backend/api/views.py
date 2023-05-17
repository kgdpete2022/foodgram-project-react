from django.contrib.auth import get_user_model
from django.shortcuts import render
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from users.models import Follow

from .serializers import (
    FollowSerializer,
    IngredientSerializer,
    RecipeIngredientSerializer,
    RecipesSerializer,
    TagSerializer,
    UserSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    pagination_class = PageNumberPagination


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class RecipeIngredientsViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer

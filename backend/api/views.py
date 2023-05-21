from django.contrib.auth import get_user_model
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from users.models import Follow

from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
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
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

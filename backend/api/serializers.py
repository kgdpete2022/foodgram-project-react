from django.db import models
from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag,
    ShoppingList,
    Favorites,
)

from users.models import User, Follow

class UserSerializer(serializers.)
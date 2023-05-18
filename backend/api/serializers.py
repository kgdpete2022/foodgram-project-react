import base64

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import serializers
from users.models import Follow

User = get_user_model()


class UserSerializer(UserSerializer):
    """Сериализатор пользователя"""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_subscribed",
        )

    def get_is_subscribed(self, other_user):
        """Проверяет подписку текущего пользователя /
        на другого пользователя (other_user)"""
        current_user = self.context.get("request").user
        if other_user == current_user or current_user.is_anonymous:
            return False
        return other_user.followed_by.filter(user=current_user).exists()


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = (
            "recipe",
            "ingredient",
            "quantity",
        )


class IngredientSerializer(serializers.ModelSerializer):
    quantity = RecipeIngredientSerializer(read_only=True)

    class Meta:
        model = Ingredient
        fields = (
            "name",
            "unit",
            "quantity",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = "__all__"


class FollowSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    follower = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = (
            "author",
            "follower",
        )

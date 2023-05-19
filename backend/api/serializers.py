import base64

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import serializers
from users.models import Follow

User = get_user_model()


class UserSerializer(UserSerializer):
    """Сериализатор отображения пользователя."""

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
        на другого пользователя (other_user)."""
        current_user = self.context.get("request").user
        if other_user == current_user or current_user.is_anonymous:
            return False
        return other_user.followed_by.filter(user=current_user).exists()


class UserCreateSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя."""

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )


class UserSubscriptionsSerializer(UserSerializer):
    """Сериализатор вывода подписок текущего пользователя."""

    recipes = RecipeSerializer(many=True, read_only=True)
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        read_only_fields = "__all__"

    def get_recipes_count(self, author):
        """Возвращает общее количество рецептов автора."""
        return author.recipes.count()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = "__all__"
        read_only_fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        model = Tag
        fields = "__all__"
        read_only_fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""

    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "text",
            "author",
            "cooking_time",
            "tags",
            "image",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
        )

    def ingredients(self, recipe):
        """Возвращает список ингредиентов рецепта."""
        pass

    def get_is_favorited(self, recipe):
        """Проверяет, добавлен ли рецепт в избранное текущего пользователя."""
        pass

    def get_is_in_shopping_cart(self, recipe):
        """Проверяет, добавлен ли рецепт /
        в список покупок текущего пользователя."""

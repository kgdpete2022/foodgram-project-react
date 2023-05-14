from django.contrib.auth import get_user_model
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import serializers
from users.models import Follow

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
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
        fields = (
            "name",
            "author",
            "image",
            "description",
            "ingredients",
            "tags",
        )


class FollowSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    follower = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = (
            "author",
            "follower",
        )

import base64

from django.contrib.auth import get_user_model
from django.db.models import F
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import serializers
from users.models import Follow

User = get_user_model()


class CustomUserSerializer(UserSerializer):
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
        return other_user.followed_by.filter(follower=current_user).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
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


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        model = Tag
        fields = "__all__"


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор вывода рецептов."""

    author = CustomUserSerializer(read_only=True)
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
        ingredients = recipe.ingredients.values(
            "id", "name", "measurement_unit", amount=F("recipe__amount")
        )
        return ingredients

    def get_is_favorited(self, recipe):
        """Проверяет, добавлен ли рецепт в избранное текущего пользователя."""
        current_user = self.context.get("request").user
        if current_user.is_anonymous:
            return False
        return current_user.favorite_recipes.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        """Проверяет, добавлен ли рецепт /
        в список покупок текущего пользователя."""
        current_user = self.context.get("request").user
        if current_user.is_anonymous:
            return False
        return current_user.shopping_list.filter(recipe=recipe).exists()


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = "__all__"


class RecipePostSerializer(serializers.ModelSerializer):
    """Сериализатор создания рецепта."""

    ingredients = RecipeIngredientSerializer(
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        error_messages={"does_not_exist": "Указанного тега не существует"},
    )
    image = Base64ImageField(max_length=None)
    author = CustomUserSerializer(read_only=True)
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def validate_tags(self, tags):
        for tag in tags:
            if not Tag.objects.filter(id=tag.id).exists():
                raise serializers.ValidationError(
                    "Указанного тега не существует"
                )
        return tags

    def validate_cooking_time(self, cooking_time):
        if cooking_time < 1:
            raise serializers.ValidationError(
                "Время готовки должно быть не меньше одной минуты"
            )
        return cooking_time

    def validate_ingredients(self, ingredients):
        ingredients_list = []
        if not ingredients:
            raise serializers.ValidationError("Отсутствуют ингридиенты")
        for ingredient in ingredients:
            if ingredient["id"] in ingredients_list:
                raise serializers.ValidationError(
                    "Ингридиенты должны быть уникальны"
                )
            ingredients_list.append(ingredient["id"])
            if int(ingredient.get("amount")) < 1:
                raise serializers.ValidationError(
                    "Количество ингредиента больше 0"
                )
        return ingredients

    @staticmethod
    def create_ingredients(recipe, ingredients):
        ingredient_liist = []
        for ingredient_data in ingredients:
            ingredient_liist.append(
                IngredientRecipe(
                    ingredient=ingredient_data.pop("id"),
                    amount=ingredient_data.pop("amount"),
                    recipe=recipe,
                )
            )
        IngredientRecipe.objects.bulk_create(ingredient_liist)

    def create(self, validated_data):
        request = self.context.get("request", None)
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientRecipe.objects.filter(recipe=instance).delete()
        instance.tags.set(validated_data.pop("tags"))
        ingredients = validated_data.pop("ingredients")
        self.create_ingredients(instance, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class BriefRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор вывода рецепта с сокращенным набором полей (для подписок пользователей)."""

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class SubscribtionsSerializer(CustomUserSerializer):
    """Сериализатор вывода подписок текущего пользователя."""

    recipes = ConciseRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

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

    def get_recipes_count(self, user):
        """Возвращает общее количество рецептов пользователя."""
        return user.recipes.count()

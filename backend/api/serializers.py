from django.contrib.auth import get_user_model
from django.db.models import F
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import serializers
from users.models import Subscription

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
            "is_subscribed",
        )

    def get_is_subscribed(self, other_user):
        current_user = self.context.get("request").user
        if current_user.is_anonymous or other_user == current_user:
            return False
        return current_user.subscriptions.filter(author=other_user).exists()


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


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = (
            "name",
            "measurement_unit",
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        model = Tag
        fields = "__all__"


# class RecipeIngredientSerialzier(serializers.ModelField):
#     ingredient = serializers.SerializerMethodField()

#     class Meta:
#         model = RecipeIngredient
#         fields = ("ingredient")


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор вывода рецептов."""

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

    def get_ingredients(self, recipe):
        """Возвращает список ингредиентов рецепта."""
        return recipe.ingredients.values(
            "id",
            "name",
            "measurement_unit",
        )

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


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания рецепта."""

    ingredients = RecipeIngredientSerializer(
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        error_messages={"does_not_exist": "Указанного тега нет в базе данных"},
    )
    image = Base64ImageField(max_length=None)
    author = UserSerializer(read_only=True)
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
                    "Указанного тега нет в базе данных"
                )
        return tags

    def validate_ingredients(self, ingredients_to_validate):
        validated_ingredients = []
        if not ingredients_to_validate:
            raise serializers.ValidationError(
                "В рецепте должен быть как минимум 1 ингредиент"
            )
        for ingredient in ingredients_to_validate:
            if ingredient["id"] in validated_ingredients:
                raise serializers.ValidationError("Такой ингредиент уже есть")
            validated_ingredients.append(ingredient["id"])
            if int(ingredient.get("amount")) < 1:
                raise serializers.ValidationError(
                    "Неверно указано количество ингредиента"
                )
        return validated_ingredients

    @staticmethod
    def create_ingredients(recipe, ingredients_to_add):
        added_ingredients = []
        for ingredient in ingredients_to_add:
            added_ingredients.append(
                RecipeIngredient(
                    ingredient=ingredient.pop("id"),
                    amount=ingredient.pop("amount"),
                    recipe=recipe,
                )
            )
        RecipeIngredient.objects.bulk_create(added_ingredients)

    def create(self, validated_data):
        author = self.context.get("request").user
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        RecipeIngredient.objects.filter(recipe=instance).delete()
        instance.tags.set(validated_data.pop("tags"))
        ingredients = validated_data.pop("ingredients")
        self.create_ingredients(instance, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeGetSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class BriefRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор вывода рецепта с сокращенным набором полей /
    (для подписок, избранного и списка покупок)."""

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class SubscriptionSerializer(UserSerializer):
    """Сериализатор вывода подписок текущего пользователя."""

    recipes = serializers.SerializerMethodField()
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

    def validate(self, data):
        """Проверяет правильность данных перед подпиской на автора."""
        author_id = (
            self.context.get("request").parser_context.get("kwargs").get("id")
        )
        author = get_object_or_404(User, id=author_id)
        user = self.context.get("request").user
        if author.followed_by.filter(id=user.id).exists():
            raise serializers.ValidationError(
                detail=f"Пользователь{user} уже подписан на автора {author}",
            )
        if user == author:
            raise serializers.ValidationError(
                detail="Пользователь не может подписаться на самого себя",
            )
        return data

    def get_recipes(self, author):
        """Возвращает рецепты автора в подписках пользователя."""
        request = self.context.get("request")
        limit = request.GET.get("recipes_limit")
        recipes = author.recipes.all()
        if limit:
            recipes = recipes[: int(limit)]
        serializer = BriefRecipeSerializer(recipes, many=True, read_only=True)
        return serializer.data

    def get_recipes_count(self, author):
        """Возвращает общее количество рецептов автора /
        в подписках пользователя."""
        return author.recipes.count()

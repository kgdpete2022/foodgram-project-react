from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

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
            # "is_subscribed",
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


class FollowSerializer(CustomUserSerializer):
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

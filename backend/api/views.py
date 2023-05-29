from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import (
    Favorites,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingList,
    Tag,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# from .filters import IngredientFilter, RecipeFilter
from rest_framework.response import Response
from users.models import Subscription

from .pagination import ViewLevelPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (
    BriefRecipeSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeGetSerializer,
    SubscriptionSerializer,
    TagSerializer,
    UserSerializer,
)

# from django_filters.rest_framework import DjangoFilterBackend


User = get_user_model()


# Create your views here.
class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = ViewLevelPagination

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)

        if user == author:
            return Response(
                {"errors": "Нельзя подписаться на самого себя"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.method == "POST":
            serializer = SubscriptionSerializer(
                author, data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                Subscription.objects.create(user=user, author=author)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == "DELETE":
            subscription = get_object_or_404(
                Subscription, user=user, author=author
            )
            if subscription.exists():
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"errors": "Пользователь не подписан на данного автора"}
            )
        return None

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)


class IngredientViewSet(viewsets.ModelViewSet):
    """Представление ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [
        IsAdminOrReadOnly,
    ]
    # filter_backends = [IngredientFilter, ]
    # search_fields = ['^name', ]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление рецептов."""

    queryset = Recipe.objects.all()
    # pagination_class = ViewLevelPagination
    permission_classes = [
        IsOwnerOrReadOnly,
    ]
    # filter_backends = [DjangoFilterBackend, ]
    # filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipeGetSerializer
        return RecipeCreateSerializer

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def shopping_cart(self, request, pk):
        if ShoppingList.objects.filter(
            user=request.user, recipe__id=pk
        ).exists():
            return Response(
                {"errors": "Рецепт уже есть списке покупок"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        recipe = get_object_or_404(Recipe, id=pk)
        ShoppingList.objects.create(user=request.user, recipe=recipe)
        serializer = BriefRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def destroy_shopping_cart(self, request, pk):
        if not Recipe.objects.filter(id=pk).exists():
            return Response({"errors": "Такого рецепта нет в базе"})
        obj = ShoppingList.objects.filter(user=request.user, recipe__id=pk)
        if not obj.exists():
            return Response({"errors": "Этого рецепта нет в списке покупок"})
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        if Favorites.objects.filter(user=request.user, recipe__id=pk).exists():
            return Response(
                {"errors": "Рецепт уже есть избранном"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        recipe = get_object_or_404(Recipe, id=pk)
        Favorites.objects.create(user=request.user, recipe=recipe)
        serializer = BriefRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def destroy_favorite(self, request, pk):
        if not Recipe.objects.filter(id=pk).exists():
            return Response({"errors": "Такого рецепта нет в базе"})
        obj = Favorites.objects.filter(user=request.user, recipe__id=pk)
        if not obj.exists():
            return Response({"errors": "Этого рецепта нет в избранном"})
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=["get"], permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        current_user = request.user
        shopping_list = f"Cписок покупок пользователя {current_user}:\n"
        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__added_to_shopping_list__user=current_user
            )
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(amount=Sum("amount"))
        )
        for num, ing in enumerate(ingredients):
            shopping_list += (
                f"{num + 1}. {ing['ingredient__name']} - {ing['amount']}"
                / f"{ing['ingredient__measurement_unit']}\n"
            )

        filename = f"shopping-list_{request.user}.txt"
        response = HttpResponse(
            shopping_list, content_type="text/plain; charset=utf-8"
        )
        response["Content-Disposition"] = f"attachment; filename='{filename}'"
        return response

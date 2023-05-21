from django.contrib.auth import get_user_model
from django.db.models.import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
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
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from .pagination import ViewLevelPagination
from .permissions import isAuthor
from .serializers import (
    FavoritesSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeGetSerializer,
    ShoppingListSerializer,
    TagSerializer,
    UserSerializer,
)

User = get_user_model()


class IngredientViewSet(viewsets.ModelViewSet):
    """Представление ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление рецептов."""

    queryset = Recipe.objects.all()
    pagination_class = ViewLevelPagination
    permission_classes = (isAuthor,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipeGetSerializer
        return RecipeCreateSerializer

    @action(
        detail=True,
        methods=("POST",),
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        data = {"user": request.user.id, "recipe": recipe.id}
        serializer = ShoppingListSerializer(
            data=data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @shopping_cart.mapping.delete
    def destroy_shopping_cart(self, request, pk):
        get_object_or_404(
            ShoppingList,
            user=request.user.id,
            recipe=get_object_or_404(Recipe, id=pk),
        ).delete()

    @action(
        detail=True,
        methods=("POST",),
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        data = {"user": request.user.id, "recipe": recipe.id}
        serializer = FavoritesSerializer(
            data=data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @shopping_cart.mapping.delete
    def destroy_favorite(self, request, pk):
        get_object_or_404(
            Favorites,
            user=request.user.id,
            recipe=get_object_or_404(Recipe, id=pk),
        ).delete()

    @action(
        detail=False, methods=["get"], permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(request):
        current_user = request.user
        ingredient_list = f"Cписок покупок пользователя {current_user}:\n"
        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__added_to_shopping_list__user=current_user
            )
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(amount=Sum("amount"))
        )
        for num, ing in enumerate(ingredients):
            ingredient_list += (
                f"{num + 1}. {ing['ingredient__name']} - {ing['amount']}"
                / f"{ing['ingredient__measurement_unit']}\n"
            )

        filename = f"shopping-list_{request.user},pdf"
        response = HttpResponse(
            ingredient_list, "Content-Type: application/pdf"
        )
        response["Content-Disposition"] = f"attachment; filename='{filename}'"
        return response


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

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
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeGetSerializer,
    TagSerializer,
    UserSerializer,
    BriefRecipeSerializer,
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
        methods=["post"],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        if ShoppingList.objects.filter(user=request.user, recipe__id=pk).exists():
            return Response({"errors": "Рецепт уже есть списке покупок!"}, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        ShoppingList.objects.create(user=request.user, recipe=recipe)
        serializer = BriefRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @shopping_cart.mapping.delete
    def destroy_shopping_cart(self, request, pk):
        if not Recipe.objects.filter(id=pk).exists():
            return Response({"errors": "Такого рецепта нет в базе!"})
        obj = ShoppingList.objects.filter(user=request.user, recipe__id=pk)
        if not obj.exists():
            return Response({"errors": "Этого рецепта нет в списке покупок!"})
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        if Favorites.objects.filter(user=request.user, recipe__id=pk).exists():
            return Response({"errors": "Рецепт уже есть избранном"}, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        Favorites.objects.create(user=request.user, recipe=recipe)
        serializer = BriefRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @favorite.mapping.delete
    def destroy_favorite(self, request, pk):
        if not Recipe.objects.filter(id=pk).exists():
            return Response({"errors": "Такого рецепта нет в базе!"})
        obj = Favorites.objects.filter(user=request.user, recipe__id=pk)
        if not obj.exists():
            return Response({"errors": "Этого рецепта нет в избранном!"})
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)       



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

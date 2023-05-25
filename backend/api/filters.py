from django_filters import rest_framework
from rest_framework.filters import SearchFilter

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(SearchFilter):
    search_param = "name"

    class Meta:
        model = Ingredient
        fields = ("name",)

class RecipeFilter(rest_framework.FilterSet):
    author = rest_framework.CharFilter()
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=Tag.objects.all(),
        label="Теги",
        to_field_name="slug"
    )
    is_favorited = rest_framework.BooleanFilter(method="get_favorite")
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method="get_is_in_shopping_cart")

    class Meta:
        model = Recipe
        fields = ("tags", "author", "is_favorited", "is_in_shopping_cart")

    def get_favorite(self, queryset, name, value):
        if value:
            return queryset.filter(favorite_recipes__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_list__user=self.request.user)
        return queryset

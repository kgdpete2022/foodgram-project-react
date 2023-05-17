from django.contrib import admin

from .models import (
    Favorites,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingList,
    Tag,
)


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color")
    list_editable = ("color",)
    search_fields = ("name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_dispay = (
        "name",
        "unit_name",
        "quantity",
    )

    search_fields = ("name",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "author",
        "image",
        "cooking_time",
    )
    inlines = (IngredientInline,)

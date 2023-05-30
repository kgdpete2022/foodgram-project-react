from django.contrib import admin

from .models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag,
    RecipeTag,
    Favorites,
    ShoppingList,
)


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1


class TagInline(admin.TabularInline):
    model = RecipeTag
    min_num = 1


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color")
    list_editable = ("color",)
    search_fields = ("name",)


class IngredientAdmin(admin.ModelAdmin):
    list_dispay = (
        "name",
        "unit_name",
        "quantity",
    )
    search_fields = ("name",)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "author",
        "image",
        "cooking_time",
    )
    inlines = (
        IngredientInline,
        TagInline,
    )


class FavoritesAdmin(admin.ModelAdmin):
    model = Favorites


class ShoppingListAdmin(admin.ModelAdmin):
    model = ShoppingList


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)

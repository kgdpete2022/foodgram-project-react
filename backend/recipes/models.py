from django.conf import settings
from django.db import models


class Ingredient(models.Model):
    """Модель ингредиента"""

    name = models.CharField(
        max_length=settings.FIELD_LENGTH["M"],
        verbose_name="Название ингредиента",
        unique=True,
        db_index=True,
    )
    unit = models.CharField(
        max_length=settings.FIELD_LENGTH["M"],
        verbose_name="Единица измерения",
    )

    def __str__(self):
        return f"{self.name}, {self.unit}"

    class Meta:
        ordering = ("name",)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "unit"], name="unique_name_unit"
            )
        ]


class Tag(models.Model):
    """Модель тега"""

    name = models.CharField(
        max_length=settings.FIELD_LENGTH["M"],
        verbose_name="Название",
        db_index=True,
    )
    color = models.CharField(
        max_length=settings.FIELD_LENGTH["CUSTOM_HEX"],
        verbose_name="Цветовой код (hex)",
        unique=True,
    )
    slug = models.SlugField(
        max_length=settings.FIELD_LENGTH["M"],
        verbose_name="URL-путь к данному тэгу",
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Recipe(models.Model):
    """Модель рецепта"""

    name = models.CharField(
        max_length=settings.FIELD_LENGTH["L"],
        verbose_name="Название рецепта",
        help_text="Добавьте название рецепта",
        db_index=True,
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта",
        help_text="Выберите автора рецепта из списка",
    )

    image = models.ImageField(
        upload_to="recipes/images/",
        verbose_name="Изображение",
        help_text="Добавьте фото к рецепту",
    )

    description = models.TextField(
        verbose_name="Описание рецепта",
        help_text="Добавьте подробное описание рецепта",
    )

    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient", verbose_name="Ингредиенты"
    )

    tags = models.ManyToManyField(Tag, verbose_name="Теги")
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления (в минутах)"
    )

    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Время публикации"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
    )
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient",
            )
        ]


class Favorites(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorite_recipes",
        verbose_name="Пользователь, добавивший в избранное",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="added_to_favorites",
        verbose_name="Рецепт, добавленный в избранное",
    )

    def __str__(self):
        return f"Рецепт {self.recipe} в избранном пользователя {self.user}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_user_recipe_favorites"
            )
        ]


class ShoppingList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shopping_list",
        verbose_name="Пользователь, добавивший в список покупок",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="added_to_shopping_list",
        verbose_name="Рецепт",
    )

    def __str__(self):
        return (
            f"Рецепт {self.recipe} в списке покупок пользователя {self.user}"
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_user_recipe_shopping_list",
            )
        ]

from django.db import models
from django.contrib.auth.models import User
from foodgram.settings import FIELD_LENGTH


class Ingredient(models.Model):
    """Модель ингредиента"""

    name = models.CharField(
        max_length=FIELD_LENGTH["MID_LENGTH"],
        verbose_name="Название",
    )
    unit_name = models.CharField(
        max_length=FIELD_LENGTH["MID_LENGTH"],
        verbose_name="Единица измерения",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"


class Tag(models.Model):
    """Модель тега"""

    name = models.CharField(
        max_length=FIELD_LENGTH["MID_LENGTH"], verbose_name="Название"
    )
    hex_code = models.CharField(
        max_length=FIELD_LENGTH["TAG_HEX_CODE_LENGTH"],
        verbose_name="Цветовой код (hex)",
    )
    slug = models.SlugField(
        unique=True, verbose_name="URL-путь к данному тэгу"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Recipe(models.Model):
    """Модель рецепта"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
        help_text="Выберите автора из списка",
    )
    name = models.CharField(
        max_length=FIELD_LENGTH["LARGE_LENGTH"],
        verbose_name="Название",
        help_text="Добавьте название рецепта",
    )
    image = models.ImageField(
        upload_to="recipes/images",
        verbose_name="Изображение",
        help_text="Добавьте фото к рецепту",
    )

    description = models.TextField(
        verbose_name="Описание рецепта", help_text="Добавьте описание рецепта"
    )
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient", verbose_name="Ингредиенты"
    )
    tags = models.ManyToManyField(Tag, verbose_name="Теги")
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество")

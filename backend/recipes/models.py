from django.db import models
from django.contrib.auth.models import User
from foodgram.settings import FIELD_LENGTH


class Ingredient(models.Model):
    """Модель ингредиента"""

    name = models.CharField(
        max_length=FIELD_LENGTH["MID_LENGTH"],
        verbose_name="Название ингредиента",
        unique=True,
        db_index=True,
    )
    unit = models.CharField(
        max_length=FIELD_LENGTH["MID_LENGTH"],
        verbose_name="Единица измерения",
    )

    def __str__(self):
        return f"{self.name}, {self.unit}"

    class Meta:
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
        max_length=FIELD_LENGTH["MID_LENGTH"],
        verbose_name="Название",
        db_index=True,
    )
    hex_code = models.CharField(
        max_length=FIELD_LENGTH["TAG_HEX_CODE_LENGTH"],
        verbose_name="Цветовой код (hex)",
        unique=True,
    )
    slug = models.SlugField(
        max_length=FIELD_LENGTH["MID_LENGTH"],
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
        max_length=FIELD_LENGTH["LARGE_LENGTH"],
        verbose_name="Название рецепта",
        help_text="Добавьте название рецепта",
    )

    author = models.ForeignKey(
        User,
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
        Ingredient, through="IngredientQuantity", verbose_name="Ингредиенты"
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


class IngredientQuantity(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="+"
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество")


class Favorites(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="Рецепт"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_user_recipe"
            )
        ]

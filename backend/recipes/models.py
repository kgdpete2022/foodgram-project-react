from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')
    quantity = models.IntegerField(verbose_name='Количество')
    unit_name = models.CharField(
        max_length=60, verbose_name='Единица измерения'
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')
    hex_code = models.CharField(
        max_length=7, verbose_name='Цветовой код (hex)'
    )
    slug = models.SlugField(
        unique=True, verbose_name='URL-путь к данному тэгу'
    )

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(
        upload_to='media/images',
        blank=True,
        verbose_name='Изображение',
        help_text='Загрузите изображение',
    )
    alt = models.CharField(
        max_length=100,
        verbose_name='Описание',
        help_text='Добавьте описание изображения для использования в alt-атрибуте',
    )


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Выберите автора из списка',
    )
    name = models.CharField(
        max_length=60,
        verbose_name='Название',
        help_text='Добавьте название рецепта',
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
    )

    description = models.TextField(
        verbose_name='Описание рецепта', help_text='Добавьте описание рецепта'
    )
    ingredients = models.ManyToManyField(Ingredient)
    tags = models.ManyToManyField(Tag)
    cooking_time = models.FloatField()

    def __str__(self):
        return self.name

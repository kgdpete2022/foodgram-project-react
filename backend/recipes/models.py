from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(max_length=60, verbose_name='Название')
    image = models.ImageField()

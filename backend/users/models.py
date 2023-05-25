from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_username

from foodgram.settings import FIELD_LENGTH


class User(AbstractUser):
    username = models.CharField(
        max_length=FIELD_LENGTH["S"],
        unique=True,
        verbose_name="Логин",
        help_text="Введите логин",
        validators=[validate_username],
    )

    email = models.EmailField(
        max_length=FIELD_LENGTH["XL"],
        unique=True,
        verbose_name="Электронная почта",
        help_text="Введите адрес электронной почты",
    )

    first_name = models.CharField(
        max_length=FIELD_LENGTH["S"],
        verbose_name="Имя",
        help_text="Укажите Ваше имя",
    )

    last_name = models.CharField(
        max_length=FIELD_LENGTH["S"],
        verbose_name="Фамилия",
        help_text="Укажите Вашу фамилию",
    )

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Follow(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор рецептов",
    )
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followed_by",
        verbose_name="Фолловер",
    )

    def __str__(self):
        return f"Автор {self.author} - подписчик {self.follower}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "follower"],
                name="unique_author_follower",
            )
        ]

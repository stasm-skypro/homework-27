from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Класс для определения модели Пользователя"""

    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="Адрес электронной почты",
        help_text="Введитте адрес электронной почты",
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Номер телефона",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    avatar = models.ImageField(verbose_name="Аватар", blank=True, null=True, upload_to="users/")
    country = models.CharField(max_length=50, verbose_name="Страна", help_text="Введите страну", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    
    def __str__(self):
        return self.email


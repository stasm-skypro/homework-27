from django.contrib.auth.forms import UserCreationForm
from blog.mixins import StyledFormMixin
from users.models import CustomUser


class UserRegisterForm(StyledFormMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": "Имя пользователя",
            "email": "Адрес электронной почты",
            "password1": "Пароль",
            "password2": "Подтверждение пароля",
        }
        help_texts = {
            "username": "Введите имя пользователя",
            "email": "Введите адрес электронной почты",
            "password1": "Введите пароль",
            "password2": "Подтвердите пароль",
        }

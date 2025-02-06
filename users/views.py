"""
Контроллеры, определённые внутри приложения users.
"""

from django.contrib.auth import logout, login
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import CustomUser


class UserRegisterView(CreateView):
    """Класс создания представления для регистрации пользователя."""

    model = CustomUser
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = "Добро пожаловать на сайт!"
        message = "Спасибо за регистрацию! Мы рады видеть вас среди нас."
        from_email = "stasm226@gmail.com"
        recipients = ["stasm226@gmail.com"]
        send_mail(subject, message, from_email, recipients)


class UserLoginView(LoginView):
    """Класс для создания представления входа пользователя."""

    template_name = "users/login.html"
    context_object_name = "user"

    def get_success_url(self):
        return reverse_lazy("catalog:product_list")


def custom_logout(requesst):
    """Производит выход пользователя из системы."""
    logout(requesst)
    return redirect(reverse_lazy("catalog:product_list"))


class UserLogoutView(LogoutView):
    """Класс для создания представления выхода пользователя."""

    def get(self, request, *args, **kwargs):
        """Обработчик GET-запроса для выхода"""
        logout(request)
        return redirect("catalog:product_list")


class UserUpdateView(CreateView):
    """Класс для создания представления редактирования профиля пользователя."""

    model = CustomUser
    form_class = UserUpdateForm
    template_name = "users/user_update.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

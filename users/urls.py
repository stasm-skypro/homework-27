from django.urls import path
from users.views import UserRegisterView, UserLoginView, custom_logout
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(template_name="users/login.html"), name="login"),
    path(
        "logout/",
        custom_logout,
        name="logout",
    ),
]

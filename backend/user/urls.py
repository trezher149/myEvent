from django.urls import path

from . import api

urlpatterns = [
    path("signup", api.signup, name="add_user"),
    path("login", api.login, name="login_user")
]
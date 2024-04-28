from django.urls import path

from . import api

urlpatterns = [
    path("signup", api.signup, name="add_user"),
    path("login", api.login, name="login_user"),
    path('<str:user_id>/', api.get_user_profile, name='get_user_profile'),
    path('<str:user_id>/events/', api.get_user_events, name='get_user_events'),
]
from django.urls import path

from . import api

urlpatterns = [
    path("create", api.event_create, name="event_create"),
    path("find", api.event_nearest, name="event_nearest")
]
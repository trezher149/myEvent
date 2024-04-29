from django.urls import path
from . import api

urlpatterns = [
    path("create", api.event_create, name="event_create"),
    path("find", api.event_nearest, name="event_nearest"),
    path("participants/<str:event_id>", api.list_participants, name="list_participants"),
    path("update/<str:event_id>", api.event_update, name="event_update"),
    path("participate", api.participate, name="participate"),
    path("approve/<str:event_id>", api.approve_event_view, name="approve_event"),  # เพิ่ม URL สำหรับการอนุมัติ
]

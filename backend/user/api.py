from django.http import HttpResponse, HttpRequest, QueryDict
from .models import user
import json

def signup(request: HttpRequest):
    db_name = user.create_user("test", "test", "test")
    return HttpResponse(db_name)

def login(request: HttpRequest):
    if request.method == "POST":
        login_info = json.loads(request.body)
        user_id = user.login_user(login_info["username"], login_info["password"])
        if not user_id:
            return HttpResponse(403)
        return HttpResponse(user_id)
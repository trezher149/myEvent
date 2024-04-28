from django.http import HttpResponse, HttpRequest
from .models import user, user_event
import json

def signup(request: HttpRequest):
    if request.method == "GET":
        return
    signup_info = request.POST.dict()
    username_taken = False
    email_taken = False
    if user.find_email(signup_info["email"]):
        email_taken = True
    if user.find_username(signup_info["username"]):
        username_taken = True
    
    response = HttpResponse()
    if username_taken or email_taken:
        response.status_code = 403
        response.content = json.dumps({"usernameTaken": username_taken,
                                       "emailTaken": email_taken})
        return response
    id = user.create_user(signup_info["email"],
                               signup_info["username"],
                               signup_info["password"])
    response.content = json.dumps({"userId": id})
    return response

def login(request: HttpRequest):
    if request.method == "POST":
        login_info = request.POST.dict()
        user_id = user.login_user(login_info["username"], login_info["password"])
        response = HttpResponse()
        if not user_id:
            response.status_code = 403
            return response
        response.content = json.dumps({"userId": user_id})
        return response
    


def get_user_profile(request: HttpRequest, user_id: str):
    if request.method == "GET":
        user_profile = user.user_profile(user_id)
        if not user_profile:
            response = HttpResponse(status=404)
            return response

        user_info = {
            "user_id": user_profile["user_id"],
            "email": user_profile["email"],
            "username": user_profile["username"],
        }

        response = HttpResponse(json.dumps(user_info), content_type="application/json")
        return response


def get_user_events(request: HttpRequest, user_id: str):
    if request.method == "GET":
        user_events = user_event.get_user_events(user_id)
        if not user_events:
            response = HttpResponse(status=404)
            return response

        response_data = {
            "user_id": user_events["user_id"],
            "event_participate": user_events["event_participate"],
            "event_create": user_events["event_create"]
        }

        response = HttpResponse(json.dumps(response_data), content_type="application/json")
        return response


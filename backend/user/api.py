from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import user, user_event
import json

from django.http import HttpResponse, HttpRequest
from .models import user
import json

def signup(request: HttpRequest):
    if request.method == "GET":
        return HttpResponse(status=405)  

    signup_info = request.POST.dict()
    email = signup_info.get("email")
    username = signup_info.get("username")
    password = signup_info.get("password")
    gender = signup_info.get("gender")
    age = signup_info.get("age")
    favorite = signup_info.get("favorite")


    if user.find_email(email):
        response_data = {"error": "Email is already taken"}
        return HttpResponse(json.dumps(response_data), status=403)
    if user.find_username(username):
        response_data = {"error": "Username is already taken"}
        return HttpResponse(json.dumps(response_data), status=403)

    
    user_id = user.create_user(email, username, password, gender, age, favorite)

    
    response_data = {"userId": user_id}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


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
            "gender": user_profile["gender"],
            "age": user_profile["age"],
            "favorite": user_profile["favorite"],
        }

        response = HttpResponse(json.dumps(user_info), content_type="application/json")
        return response


def get_user_events(request: HttpRequest, user_id: str):
    if request.method == "GET":
        events = user_event.get_user_events(user_id)
        data = {
            "userId": user_id,
            "events": events
        }

        return JsonResponse(data)


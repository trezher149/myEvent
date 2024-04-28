from django.http import HttpResponse, HttpRequest
from .models import user
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
    db_name = user.create_user(signup_info["email"],
                               signup_info["username"],
                               signup_info["password"])
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
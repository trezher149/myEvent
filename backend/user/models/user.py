from utils import get_db_handle
from pymongo import MongoClient
from uuid import uuid4, UUID

user_model = {
    "user_id": "",
    "email": "",
    "username": "",
    "password": "",
}

def create_user(email, username, password, infos={}):
    db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
    table = db["users"]
    id = str((uuid4().hex)[:6])
    user_model["user_id"] = id
    user_model["email"] = email 
    user_model["username"] = username
    user_model["password"] = password
    table.insert_one(user_model)
    return id

def login_user(username, password):
    db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
    table = db["users"]
    user =  table.find_one({"username": username})
    if not user["password"] == password:
        return False
    return user["user_id"]

def find_email(email):
    db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
    table = db["users"]
    user =  table.find_one({"email": email})
    if user : 
        return user["user_id"]
    return None

def find_username(username):
    db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
    table = db["users"]
    user =  table.find_one({"username": username})
    if user : 
        return user["user_id"]
    return None

def user_profile(user_id):
    db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
    table = db["users"]
    user = table.find_one({"user_id": user_id})
    if user:
        user_profile = {
            "user_id": user["user_id"],
            "email": user["email"],
            "username": user["username"],
        }
        return user_profile
    else:
        return None



    
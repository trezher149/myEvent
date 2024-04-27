from utils import get_db_handle
from pymongo import MongoClient
from uuid import uuid4, UUID

user_model = {
    "user_id": "",
    "email": "",
    "username": "",
    "password": "",
}

def create_user(email, username, password):
    db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
    users = db["users"]
    id = str((uuid4().hex)[:6])
    user_model["user_id"] = id
    user_model["email"] = email 
    user_model["username"] = username
    user_model["password"] = password
    return user_model

def login_user(username, password):
    db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
    users = db["users"]
    user =  users.find_one({"username": username})
    print(user)
    if not user["password"] == password:
        return False
    return user["user_id"]

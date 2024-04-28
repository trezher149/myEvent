from utils import get_db_handle
from uuid import uuid4

user_event = {
    "user_id": "",
    "event_participate": [],
    "event_create": []
}

#Under Construction
def get_user_events(user_id):
    db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
    table = db["user_events"]
    user_events = table.find_one({"user_id": user_id})
    return user_events
from utils import get_db_handle
from uuid import uuid4
import cv2 as cv
import numpy as np
import base64

user_event = {
    "user_id": "",
    "event_participate": [],
    "event_create": []
}

#Under Construction
def get_user_events(user_id):
    db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
    table = db["participants"]
    print(table.count_documents({"userId": user_id}))
    cursor = table.find({"userId": user_id})
    event_participated = list(cursor)
    for e in event_participated:
        del e["userId"]
        del e["createAt"]
    events = [] 
    table = db["events"]
    for e in event_participated:
        event = table.find_one({"eventId": e["eventId"]})
        del event["_id"]
        image = cv.imread(event["imageLocation"], flags=cv.IMREAD_COLOR)
        del event["imageLocation"]
        is_success, img_buf_arr = cv.imencode(".jpg", image)
        byte_arr = img_buf_arr.tobytes()
        event["imageBase64"] = base64.b64encode(byte_arr).decode('ascii')
        events.append(event)
    return events
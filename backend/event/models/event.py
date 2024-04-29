from utils import get_db_handle
import base64
from datetime import datetime
import cv2 as cv
from uuid import uuid4
from pymongo import GEOSPHERE 
from bson.son import SON
from geopy.distance import great_circle
import numpy as np
from io import BytesIO
from pathlib import Path
from datetime import datetime, timedelta

event = {
    "eventId": "",
    "owner": "",
    "type": "",
    "ageMin": 0,
    "ageMax": 0,
    "imageLocation": "",
    "title": "",
    "description": "",
    "locationText": "",
    "eventStart": None,
    "eventEnd": None,
    "durationDays": 1,
    "location": None,
    "createdAt": None,
    "editedAt": None,
    "hasEdited": False,
    "waitForApproval": True,
    "isApproved": False,
    "approvedAt": None
}

def create_event(event_info, image):
    event["eventId"] = str(uuid4().hex)[:6]
    arr = np.asarray(bytearray(image), dtype=np.uint8)
    img = cv.imdecode(arr, flags=cv.IMREAD_COLOR)
    cwd = Path.cwd()
    folder = Path(cwd / "event_image")
    if not folder.exists():
        (cwd / "event_image").mkdir()
    cv.imwrite(f'{cwd}/event_image/{event["eventId"]}.jpg', img)
    event["imageLocation"] = f'{cwd}/event_image/{event["eventId"]}.jpg'
    event["owner"] = event_info["userId"]
    event["type"] = event_info["type"]
    event["ageMin"] = int(event_info["ageMin"])
    event["ageMax"] = int(event_info["ageMax"])
    event["title"] = event_info["title"]
    event["description"] = event_info["description"]
    event["locationText"] = event_info["locationText"]
    event["location"] = [float(event_info["long"]), float(event_info["lat"])]
    event["createdAt"] = datetime.today().isoformat()
    event["editedAt"] = datetime.today().isoformat()
    event["eventStart"] = event_info["eventStart"]
    event["eventEnd"] = event_info["eventEnd"]
    start = datetime.fromisoformat(event["eventStart"])
    end = datetime.fromisoformat(event["eventEnd"])
    event["durationDays"] = 1 + ((end - start).days)
    db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
    table = db["events"]
    table.create_index([("location", GEOSPHERE)], unique=False)
    table.insert_one(event)
    return event["eventId"]

def find_event(longlat: list, event_type="", age_min=0, age_max=0, title=""):
    try:
        max_distance_radians = 10000 / 6371000
        query = {"location": SON([("$nearSphere", longlat), ("$maxDistance", max_distance_radians)])}
        if event_type:  # แก้ไขการตรวจสอบประเภทกิจกรรม
            print("type")
            query["type"] = event_type
        if age_min > 0:
            print("ageMin")
            query["ageMin"] = {"$gte": age_min}
        if age_max > 0:
            print("ageMax")
            query["ageMax"] = {"$lte": age_max}
        db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
        table = db["events"]

        # Problem with this fricking fuction
        cursor = table.find(query).sort({'_id': -1})
        print(cursor)
        data = list(cursor) 
        if cursor.retrieved == 0:
            return []
        cursor.close()

        for d in data:
            image = cv.imread(d["imageLocation"], flags=cv.IMREAD_COLOR)
            is_success, img_buf_arr = cv.imencode(".jpg", image)
            del d["_id"]
            del d["imageLocation"]
            # d["editedAt"] = d["editedAt"].isoformat()
            # d["eventStart"] = d["eventStart"].isoformat()
            # d["eventEnd"] = d["eventEnd"].isoformat()
            d["distance"] = great_circle((longlat[1], longlat[0]), (d["location"][1], d["location"][0])).meters
            byte_arr = img_buf_arr.tobytes()
            d["imageBase64"] = base64.b64encode(byte_arr).decode('ascii')
            print(d["imageBase64"])
        data = sorted(data, key=lambda d: d["distance"])
        return data
    except Exception as e:
        print(f"An error occurred while finding events: {e}")
        return []

#------------------------------------------- approve


def approve_event(event_id):
    try:
        db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
        table = db["events"]
        # ทำการอัปเดตสถานะเป็นอนุมัติ
        table.update_one({"eventId": event_id}, {"$set": {"isApproved": True, "approvedAt": datetime.today()}})
        return True
    except Exception as e:
        print(f"An error occurred while approving event: {e}")
        return False

def approve_event_view(request, event_id):
    if request.method == 'POST':
        success = api.approve_event(event_id)
        if success:
            return JsonResponse({"message": "Event approved successfully"}, status=200)
        else:
            return JsonResponse({"message": "Failed to approve event"}, status=400)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)





def event_update(event_id, update_info, image_byte):
    try:
        # ทำการอัปเดตข้อมูลของกิจกรรมที่มี eventId ตรงกับ event_id ด้วยข้อมูลใหม่จาก update_info
        db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
        table = db["events"]
        table.update_one({"eventId": event_id}, {"$set": update_info})
        return True
    except Exception as e:
        print(f"An error occurred while updating event: {e}")
        return False

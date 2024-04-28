from utils import get_db_handle
import json
from datetime import datetime
import cv2 as cv
from uuid import uuid4
from pymongo import GEOSPHERE 
from bson.son import SON
from geopy.distance import great_circle
import numpy as np
from io import BytesIO
from pathlib import Path
import pprint

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

participant = {
    "eventId": "",
    "participantId": "",
    "joinedAt": None,
    "validUntil": None
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
    print(event["location"])
    event["createdAt"] = datetime.today()
    event["editedAt"] = datetime.today()
    event["eventStart"] = datetime.fromisoformat(event_info["eventStart"])
    event["eventEnd"] = datetime.fromisoformat(event_info["eventEnd"])
    event["durationDays"] = 1 + ((event["eventEnd"] - event["eventStart"]).days)
    db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
    table = db["events"]
    # table.create_index([("location", GEOSPHERE)], unique=False)
    table.insert_one(event)
    return event["eventId"]

def find_event(longlat: list, event_type="", age_min=0, age_max=0, title=""):
    db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
    table = db["events"]
    max_distance_radians = 10000 / 6371000
    query = {"location": SON([("$nearSphere", longlat), ("$maxDistance", max_distance_radians)])}
    print(query)
    if len(event_type) > 0:
        query["type"] = type
    if age_min > 0:
        query["ageMin"] = {"$gte": age_min}
    if age_max > 0:
        query["ageMax"] = {"$lte": age_max}
    data = list(table.find(query))

    print(data)
    for d in data:
        d["editedAt"] = d["editedAt"].isoformat()
        d["eventStart"] = d["eventStart"].isoformat()
        d["eventEnd"] = d["eventEnd"].isoformat()
        d["distance"] = great_circle((longlat[1], longlat[0]), (d["location"][1], d["location"][0])).meters
    print(type(data))
    return data

def list_participants(event_id):
    try:
        db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
        table = db["participants"]
        # ใช้ find เพื่อค้นหาผู้เข้าร่วมกิจกรรมทั้งหมดที่มี eventId ตรงกับ event_id
        participants = list(table.find({"eventId": event_id}))
        return participants
    except Exception as e:
        print(f"An error occurred while listing participants: {e}")
        return []


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



from datetime import datetime, timedelta

def participate(event_id, user_id):
    participant["eventId"] = event_id
    participant["participantId"] = user_id
    participant["joinedAt"] = datetime.today()
    # กำหนดวันหมดอายุเป็น 1 เดือนหลังจากวันที่เข้าร่วม
    participant["validUntil"] = participant["joinedAt"] + timedelta(days=30)
    db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
    table = db["participants"]
    table.insert_one(participant)
    return participant["eventId"]



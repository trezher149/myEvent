from utils import get_db_handle
import json
from datetime import datetime
import cv2 as cv
from uuid import uuid4
from pymongo import GEOSPHERE
from bson.son import SON
from geopy.distance import great_circle

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
    event["owner"] = event_info["userId"]
    event["type"] = event_info["type"]
    event["ageMin"] = event_info["ageMin"]
    event["ageMax"] = event_info["ageMax"]
    event["title"] = event_info["title"]
    event["description"] = event_info["description"]
    event["locationText"] = event_info["locationText"]
    event["location"] = event_info["longLat"]
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
    if len(event_type) > 0:
        query["type"] = type
    if age_min > 0:
        query["ageMin"] = {"$gte": age_min}
    if age_max > 0:
        query["ageMax"] = {"$lte": age_max}
    data = list(table.find(query, {'_id':False, 'createdAt':False, 'approvedAt':False}))
    for d in data:
        d["editedAt"] = d["editedAt"].isoformat()
        d["eventStart"] = d["eventStart"].isoformat()
        d["eventEnd"] = d["eventEnd"].isoformat()
        d["distance"] = great_circle((longlat[1], longlat[0]), (d["location"][1], d["location"][0])).meters
    print(type(data))
    return data

def event_update(event_id, update_info, image_byte):
    pass

def list_participants(event_id):
    pass


def participate(event_id, user_id):
    participant["eventId"] = event_id
    participant["participantId"] = user_id
    participant["joinedAt"] = datetime.today()
    participant["validUntil"] = None  # กำหนดวันหมดอายุได้
    db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
    table = db["participants"]
    table.insert_one(participant)
    return participant["eventId"]


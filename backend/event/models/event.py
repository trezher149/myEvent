from utils import get_db_handle
import json
from datetime import datetime
import cv2 as cv
from uuid import uuid4

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
    "latLong": (0, 0),
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

def create_event(event_info, image, latlong):
    event["eventId"] = str(uuid4().hex) 
    event["owner"] = event_info["userId"]
    event["type"] = event_info["type"]
    event["ageMin"] = event_info["ageMin"]
    event["ageMax"] = event_info["ageMax"]
    event["title"] = event_info["title"]
    event["description"] = event_info["description"]
    event["locationText"] = event_info["locationText"]
    event["latLong"] = event_info["latLong"]
    event["createdAt"] = datetime.today()
    event["editedAt"] = datetime.today()
    event["eventStart"] = datetime.fromisoformat(event_info["eventStart"])
    event["eventEnd"] = datetime.fromisoformat(event_info["eventEnd"])
    event["durationDays"] = 1 + ((event["eventEnd"] - event["eventStart"]).days)
    event["latLong"] = latlong
    db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
    table = db["events"]
    pass

def find_event(latlong, type, age_min, age_max, title):
    pass

def event_update(event_id, update_info, image_byte):
    pass

def list_participants(event_id):
    pass


def participate(event_id, user_id):
    pass
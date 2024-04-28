from django.http import HttpResponse, HttpRequest
from .models import event
import json

def event_create(request: HttpRequest):
    if request.method == "GET":
        return
    event_info = json.loads(request.body)
    image_byte = event_info["image"]
    del event_info["image"]
    response = HttpResponse()
    # try:
    event_id = event.create_event(event_info, image_byte)
    response.content = json.dumps({"eventId": event_id})
    # except:
        # response.status_code = 500
    # finally:
    return response
    

def event_nearest(request):
    if request.method == "GET":
        return
    filter = json.loads(request.body)
    nearest_event = event.find_event(filter["longLat"],
                                    filter["type"],
                                    filter["ageMin"],
                                    filter["ageMax"],
                                    filter["title"])
    return HttpResponse(json.dumps({"nearestEvent": nearest_event}))

def event_details(request):
    return HttpResponse("details")

def add_participant(request):
    return HttpResponse("details")

def join_participant(request: HttpRequest):
    if request.method != "POST":
        return HttpResponse(status=405)  # Method Not Allowed

    participant_info = json.loads(request.body)
    event_id = participant_info.get("eventId", None)
    user_id = participant_info.get("userId", None)

    if not event_id or not user_id:
        return HttpResponse(status=400)  # Bad Request

    try:
        participate(event_id, user_id)
        return HttpResponse(status=201)  # Created
    except Exception as e:
        print(f"An error occurred while adding participant: {e}")
        return HttpResponse(status=500)  # Internal Server Error


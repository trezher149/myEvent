from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import event, participant
import json
from utils import get_db_handle


def event_create(request: HttpRequest):
    if request.method == "GET":
        return
    print(request.POST.dict())
    image_byte = request.FILES.dict()["image"].read()
    print(type(image_byte))
    response = HttpResponse()
    # try:
    event_id = event.create_event(request.POST.dict(), image_byte)
    response.content = json.dumps({"eventId": event_id})
    # except:
        # response.status_code = 500
    # finally:
    return response
    

def event_nearest(request: HttpRequest):
    if request.method == "GET":
        return
    filter = request.POST.dict()
    longlat = [float(filter["long"]), float(filter["lat"])]
    # response = HttpResponse()
    nearest_events = event.find_event(longlat,
                                    filter["type"],
                                    int(filter["ageMin"]),
                                    int(filter["ageMax"]),
                                    filter["title"])
    # return HttpResponse(json.dumps({"nearestEvent": nearest_event}))
    return JsonResponse({"nearestEvents": nearest_events})
    # print(nearest_event)
    # return HttpResponse()

def event_details(request: HttpRequest, event_id):
    details = event.show_event(event_id) 
    return JsonResponse(details)

def event_update(request: HttpRequest, event_id):
    if request.method == "GET":
        return
    update_fields = request.POST.dict()
    image_byte = None
    try:
        image_byte = request.FILES.dict()["image"].read()
    except:
        pass
    finally:
        is_update = event.update_event(event_id, update_fields, image_byte)
        return JsonResponse({"isUpdate": is_update})

    

def event_approve(request: HttpRequest, event_id):
    if request.method == "GET":
        return
    is_approve = event.approve_event(event_id)
    return JsonResponse({"isApprove": is_approve})

def add_participant(request:HttpRequest):
    if request.method == "GET":
        return
    data = request.POST.dict()
    participant_id = participant.participate(data["eventId"], data["userId"])
    return JsonResponse({ "participantId": participant_id })

# def join_participant(request: HttpRequest):
#     if request.method != "POST":
#         return HttpResponse(status=405)  # Method Not Allowed

#     participant_info = json.loads(request.body)
#     event_id = participant_info.get("eventId", None)
#     user_id = participant_info.get("userId", None)

#     if not event_id or not user_id:
#         return HttpResponse(status=400)  # Bad Request

#     try:
#         event.participate(event_id, user_id)
#         return HttpResponse(status=201)  # Created
#     except Exception as e:
#         print(f"An error occurred while adding participant: {e}")
#         return HttpResponse(status=500)  # Internal Server Error

def list_participants(request, event_id):
    if request.method == 'GET':
        print(event_id)
        part = participant.get_participants(event_id)
        return JsonResponse(part, safe=False)
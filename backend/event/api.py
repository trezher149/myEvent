from django.http import HttpResponse, HttpRequest
from .models import event
import json
import base64

def event_create(request: HttpRequest):
    if request.method == "GET":
        return
    print(request.POST.dict())
    image_byte = request.FILES.dict()["image"].read()
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
    nearest_event = event.find_event(longlat,
                                    filter["type"],
                                    int(filter["ageMin"]),
                                    int(filter["ageMax"]),
                                    filter["title"])
    return HttpResponse(json.dumps({"nearestEvent": nearest_event}))
    # print(nearest_event)
    # return HttpResponse()

def event_details(request):
    return HttpResponse("details")

def add_participant(request):
    return HttpResponse("details")

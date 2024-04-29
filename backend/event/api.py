from django.http import HttpResponse, HttpRequest
from .models import event
import json
import base64
from django.http import JsonResponse

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

def join_participant(request: HttpRequest):
    if request.method != "POST":
        return HttpResponse(status=405)  # Method Not Allowed

    participant_info = json.loads(request.body)
    event_id = participant_info.get("eventId", None)
    user_id = participant_info.get("userId", None)

    if not event_id or not user_id:
        return HttpResponse(status=400)  # Bad Request

    try:
        event.participate(event_id, user_id)
        return HttpResponse(status=201)  # Created
    except Exception as e:
        print(f"An error occurred while adding participant: {e}")
        return HttpResponse(status=500)  # Internal Server Error

def list_participants(request, event_id):
    if request.method == 'GET':
        participants = list_participants(event_id)
        return JsonResponse(participants, safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])

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

def participate(event_id, user_id):
    try:
        participant["eventId"] = event_id
        participant["participantId"] = user_id
        participant["joinedAt"] = datetime.today()
        # กำหนดวันหมดอายุเป็น 1 เดือนหลังจากวันที่เข้าร่วม
        participant["validUntil"] = participant["joinedAt"] + timedelta(days=30)
        db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
        table = db["participants"]
        table.insert_one(participant)
        return participant["eventId"]
    except Exception as e:
        print(f"An error occurred while participating in the event: {e}")
        return None

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


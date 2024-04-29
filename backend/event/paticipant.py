
# ------------- จาก api

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







# ------------ event

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



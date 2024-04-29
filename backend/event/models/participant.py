from utils import get_db_handle
from datetime import datetime
from uuid import uuid4

event_part = {
    "participantId" : "",
    "eventId" : "",
    "userId" : "",
    "createAt" : None,
}
# ------------- จาก api

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

# def participate(event_id, user_id):
#     try:
#         event_part["eventId"] = event_id
#         event_part["participantId"] = user_id
#         event_part["createAt"] = datetime.today().isoformat()
#         # กำหนดวันหมดอายุเป็น 1 เดือนหลังจากวันที่เข้าร่วม
#         db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
#         table = db["participants"]
#         table.insert_one(event_part)
#         return event_part["eventId"]
#     except Exception as e:
#         print(f"An error occurred while participarting in the event: {e}")
#         return None







# ------------ event

def get_participants(event_id):
    try:
        db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
        table = db["participants"]
        # ใช้ find เพื่อค้นหาผู้เข้าร่วมกิจกรรมทั้งหมดที่มี eventId ตรงกับ event_id
        cursor = table.find({"eventId": event_id})
        if cursor.retrieved == 0:
            return []
        participants = list(cursor)
        return participants
    except Exception as e:
        print(f"An error occurred while listing participants: {e}")
        return []


def participate(event_id, user_id):
    event_part["eventId"] = event_id
    event_part["userId"] = user_id
    event_part["participantId"] = str(uuid4().hex)[:6]
    event_part["createAt"] = datetime.today().isoformat()
    # กำหนดวันหมดอายุเป็น 1 เดือนหลังจากวันที่เข้าร่วม
    db = get_db_handle("myEvent", "localhost", "27017", "root", "password")
    table = db["participants"]
    table.insert_one(event_part)
    return event_part["participantId"]

# มันจะมี dictionnary json อยู่ข้างบนสุด เเล้วก็จะมีค่าที่จะใส่เข้าไปมีอะไรบ้าง ดันใช้ตัวเเปรโดยที่ยังไม่ประกาศค่า

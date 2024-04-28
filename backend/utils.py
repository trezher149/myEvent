from pymongo import MongoClient
def get_db_handle(db_name, host, port, username, password):

    client = MongoClient(f"mongodb://{username}:{password}@{host}:{port}")
    db_handle = client[db_name]
    return db_handle
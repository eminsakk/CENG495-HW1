from pymongo import MongoClient



# Configs for the database.
ATLAS_URI = "mongodb+srv://mongo:mongo123@cluster0.va5kqxy.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "buyin"

def get_database():
    client = MongoClient(ATLAS_URI)
    db = client.buyin
    return db


# user_data format:
# {
#    "username": "test",
#    "password": "test",
#    "reviews": [{ "item_id": "123", "rating": 3}],
#    "avg_rating": 3.0
#    "is_admin": "False"
# }

def insert_user(user_data):
    db = get_database()
    users = db.users
    
    if users.find_one({"username": user_data["username"]}) is not None:
        raise Exception("User already exists")
    
    
    result = users.insert_one(user_data)
    return result.inserted_id
    
def insert_item(item_data):
    db = get_database()
    items = db.items
    result = items.insert_one(item_data)
    return result.inserted_id


def remove_user(username):
    db = get_database()
    users = db.users
    result = users.delete_one({"username": username})
    return result.deleted_count


def get_collection_items(collection_name):
    db = get_database()
    collection = db[collection_name]
    cursor = collection.find({})
    items = [item for item in cursor]
    return items
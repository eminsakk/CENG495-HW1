from pymongo import MongoClient



# Configs for the database.
ATLAS_URI = "mongodb+srv://mongo:mongo123@cluster0.va5kqxy.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "buyin"

def get_database():
    client = MongoClient(ATLAS_URI)
    db = client.buyin
    return db


def createCollections():
    db = get_database()
    try:
        db.create_collection("users")
        db.create_collection("items")
        db.create_collection("reviews")
    except Exception as e:
        
        pass
    return db.list_collection_names()



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
    
    
    
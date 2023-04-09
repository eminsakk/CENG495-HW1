from pymongo import MongoClient
from bson import ObjectId



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

def remove_item(item_id):
    db = get_database()
    users = db.items
    result = users.delete_one({"_id": ObjectId(item_id)})
    return result.deleted_count

def get_collection_items(collection_name):
    db = get_database()
    collection = db[collection_name]
    cursor = collection.find({})
    items = [item for item in cursor]
    return items

def is_eligible(username):
    db = get_database()
    collection = db.users
    
    if collection.find_one({"username": username}) is not None:
        return False
    
    return True

def insert_review(content,username,rating,item_id):
    db = get_database()
    collection = db.reviews
    result = collection.insert_one({"content":content,"username":username,"rating":rating,"item_id":item_id})
    return result.inserted_id



def add_reviews_to_user(username,review_id):
    db = get_database()
    collection = db.users
    
    try:
        query = {"username": username}
        new_values = {"$push": {"reviews": review_id}}
        collection.update_one(query,new_values)
    except Exception as e:
        print(e)
        return False
    
    return True
        
    
    
def get_reviews_for_item(item_id):
    db = get_database()
    collection = db.reviews
    cursor = collection.find({"item_id":item_id})
    reviews = [review for review in cursor]
    
    avg_rating = 0
    for review in reviews:
        avg_rating += int(review["rating"])
        
    avg_rating /= len(reviews)
    avg_rating = float("{:.2f}".format(avg_rating))
    
    return reviews,avg_rating

def remove_reviews_username(username):
    db = get_database()
    collection = db.reviews
    result = collection.delete_many({"username":username})
    return result.deleted_count

def remove_reviews_item(username):
    db = get_database()
    collection = db.reviews
    result = collection.delete_many({"item_id":username})
    return result.deleted_count

    
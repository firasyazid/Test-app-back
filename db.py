from bson import ObjectId
from pymongo.collection import Collection
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

CONNECTION_STRING = os.getenv("CONNECTION_STRING")

client = MongoClient(CONNECTION_STRING)
db = client["MedicalChatbot"]
user_collection = db["User"]

def create_user(collection: Collection, user_data: dict) -> str:
    user_data["created_at"] = datetime.utcnow()
    user_data["updated_at"] = datetime.utcnow()
    user_id = collection.insert_one(user_data).inserted_id
    return str(user_id)

def get_user_by_email(collection: Collection, email: str) -> dict:
    return collection.find_one({"email": email})

def update_user(collection: Collection, email: str, update_data: dict):
    update_data["updated_at"] = datetime.utcnow()
    collection.update_one({"email": email}, {"$set": update_data})

def delete_user(collection: Collection, email: str):
    collection.delete_one({"email": email})

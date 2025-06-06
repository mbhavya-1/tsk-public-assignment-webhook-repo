from pymongo import MongoClient

# Setup MongoDB here
# mongo = PyMongo(uri="mongodb://localhost:27017/database")
import os

MONGO_URI = os.getenv("MONGO_URI")
# print("MONGO_URI", MONGO_URI)
client = MongoClient(MONGO_URI)
db = client["webhookDB"]
collection = db["webhook_events"]
import os
from pymongo import MongoClient

# MongoDB is connected

# MONGO_URI is an environment vairable
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["webhookDB"]
collection = db["webhook_events"]
import json
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb+srv://mgbemenaosonduv:BunepSMBFPMlGrpq@cluster0.ni4jehx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["smart_transport"]
collection = db["components"]

# Load data from JSONL file
with open("data/sensor_data_stream.jsonl", "r") as f:
    for line in f:
        record = json.loads(line)
        collection.insert_one(record)

print("✅ Data inserted into MongoDB!")

print("📦 Available component_ids:")
for doc in collection.find({}, {"component_id": 1, "_id": 0}):
    print(doc["component_id"])

import json
from pymongo import MongoClient
from pymongo.errors import AutoReconnect, OperationFailure

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "maindb"
COLLECTION_NAME = "jvn"  # Changed collection name here

try:
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    print("Connected to MongoDB!")
except AutoReconnect as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()

# Load JSON data from file
json_file_path = r"C:/Users/abdul/OneDrive/Desktop/Global-Database-Reasearch/dummyab.json"

try:
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"File not found: {json_file_path}")
    exit()
except json.JSONDecodeError:
    print(f"Error decoding JSON from the file: {json_file_path}")
    exit()

# Insert data into MongoDB
try:
    if isinstance(data, list):  # Ensure it's a list of documents
        collection.insert_many(data)
    else:
        collection.insert_one(data)
    print("Data successfully inserted into MongoDB!")
except OperationFailure as e:
    print(f"Error inserting data into MongoDB: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    # Close the connection
    client.close()
    print("MongoDB connection closed.")
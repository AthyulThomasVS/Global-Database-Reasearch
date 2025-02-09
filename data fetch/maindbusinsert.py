import json
from pymongo import MongoClient
from pymongo.errors import AutoReconnect, OperationFailure

def maindbusinsert():
    MONGO_URI = "mongodb://localhost:27017/"
    DATABASE_NAME = "maindb"
    COLLECTION_NAME = "usnvd"  # Changed collection name here

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
    json_file_path = r"C:/Users/abdul/OneDrive/Desktop/Global-Database-Reasearch/cve_today.json"

    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
        exit()
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file: {json_file_path}")
        exit()

    # Insert data into MongoDB while ignoring duplicates
    try:
        if isinstance(data, list):  # Ensure it's a list of documents
            for doc in data:
                collection.update_one({"id": doc["id"]}, {"$setOnInsert": doc}, upsert=True)
        else:
            collection.update_one({"id": data["id"]}, {"$setOnInsert": data}, upsert=True)
        print("Data successfully inserted into Main US DB  (ignoring duplicates)!")
    except OperationFailure as e:
        print(f"Error inserting data into MongoDB: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Close the connection
        client.close()
        print("Main US DB connection closed.")

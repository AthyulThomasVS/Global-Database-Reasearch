import json
from pymongo import MongoClient
from pymongo.errors import AutoReconnect, OperationFailure

def jvninsert():
    MONGO_URI = "mongodb://localhost:27017/"
    DATABASE_NAME = "jvn"
    COLLECTION_NAME = "cvedatas" 

    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        print("Connected to MongoDB!")
    except AutoReconnect as e:
        print(f"Error connecting to MongoDB: {e}")
        exit()

   
    json_file_path = r"C:/Users/abdul/OneDrive/Desktop/Global-Database-Reasearch/jvn_data.json"

    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
        exit()
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file: {json_file_path}")
        exit()

    try:
        if isinstance(data, list):  
            for doc in data:
                collection.update_one({"identifier": doc["identifier"]}, {"$setOnInsert": doc}, upsert=True)
        else:
            collection.update_one({"identifier": data["identifier"]}, {"$setOnInsert": data}, upsert=True)
        print("Data successfully inserted into jvnDB (ignoring duplicates)!")
    except OperationFailure as e:
        print(f"Error inserting data into MongoDB: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        client.close()
        print("jvnDB connection closed.")

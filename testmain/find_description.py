from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")  
db = client["usnvd"]
collection = db["cvedatas"]

def find_similar_descriptions(description, min_length=10, max_length=50, step=5):
    
    for length in range(max_length, min_length - 1, -step):
        short_desc = description[:length]
        results = list(collection.find({"description": {"$regex": short_desc, "$options": "i"}}))  
        if results:  
            return results
    
    return [] 


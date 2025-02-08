from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB Database
def connect_to_database():
    client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI
    db = client['maindb']  # Replace with your MongoDB database name
    return db

# Fetch data from MongoDB
def fetch_usdata():
    db = connect_to_database()
    collection = db['usnvd']  # Replace with your collection name
    data = list(collection.find({}))  # Fetch all documents in the collection
    return data

def fetch_jvndata():
    db = connect_to_database()
    collection = db['jvn']  # Replace with your collection name
    data = list(collection.find({}))  # Fetch all documents in the collection
    return data


# API endpoint to get MongoDB data
@app.route('/api/usdata', methods=['GET'])
def get_usdata():
    data = fetch_usdata()
    
    # Convert MongoDB _id to string for JSON serialization
    for item in data:
        item['_id'] = str(item['_id'])
    
    return jsonify(data)

@app.route('/api/jvndata', methods=['GET'])
def get_jvndata():
    data = fetch_jvndata()
    
    # Convert MongoDB _id to string for JSON serialization
    for item in data:
        item['_id'] = str(item['_id'])
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

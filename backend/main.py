from flask import *
from pymongo import MongoClient

app = Flask(__name__)

#Connect to MongoDB
client = MongoClient("mongodb:27017")
db = client['demo'] 
collection = db['data']

@app.route('/')
def ping_server():
    return "Welcome to the MongoDB!"

# Add data to MongoDB route 
@app.route('/add_data', methods=['POST']) 
def add_data(): 
    # Get data from request 
    data = request.json 
  
    # Insert data into MongoDB 
    collection.insert_one(data) 
  
    return 'Data added to MongoDB'

@app.route('/get_data', methods=['GET'])
def get_data():
    #get data from db
    data = list(collection.find({}))  # Retrieve all documents
    
    # Convert ObjectId to string for JSON serialization
    for entry in data:
        entry['_id'] = str(entry['_id'])
    
    # Return data as JSON
    return jsonify(data)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5050)

from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

#Connect to MongoDB
client = MongoClient("mongo:27017")

@app.route('/')
def ping_server():
    return "Welcome to the MongoDB!"

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5050)

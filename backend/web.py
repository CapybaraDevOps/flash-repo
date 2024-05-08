from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib

app = Flask(__name__)

client = MongoClient("mongodb:27017")

# Mongodb database
db = client.flask_database

# Collection
clients = db.clients
ip_hash = db.ip_hash

@app.route("/", methods=['GET', 'POST'])
def index():
   # Get client's IP addr
   client_ip = request.remote_addr
   # Hashing IP addr
   h = hashlib.sha256(client_ip.encode()).hexdigest()
   # Check if user was in website
   if ip_hash.find_one({'hash': h}):
       return redirect(url_for('form'))
   ip_hash.insert_one({'hash': h})
   return render_template('index.html', client_ip=client_ip)


@app.route("/form", methods=['GET', 'POST'])
def form():
    # Get client's IP addr
    client_ip = request.remote_addr
    if request.method == 'POST':
        data = request.form['data']
        # Update database
        clients.insert_one({'ip': client_ip, 'data':data})
        return redirect(url_for('form'))
    all_data = clients.find()
    return render_template('form.html', client_ip=client_ip, clients=all_data)

# Delete record
@app.post("/<id>/delete/")
def delete(id):
   clients.delete_one({"_id":ObjectId(id)})
   return redirect(url_for('form'))
    

# Run web-server
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5050)


from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib

app = Flask(__name__)

#client = MongoClient("mongodb:27017")
client = MongoClient('localhost', 27017)

# Mongodb database
db = client.flask_database

# Collection
clients = db.clients

def get_hash():
    # Get client's IP addr
    client_ip = request.remote_addr
    # Hashing IP addr
    return hashlib.sha256(client_ip.encode()).hexdigest()

@app.route("/", methods=['GET', 'POST'])
def index():
   # Get client's IP addr
   client_ip = request.remote_addr

   h = get_hash()
   # Check if user was in website
   if clients.find_one({'client_ip': client_ip}):
       return redirect(url_for('form'))
   if clients.find_one({'ip_hash': h}):
       return redirect(url_for('declined'))
   if request.method == 'POST':
        # Update database
        clients.insert_one({'ip_hash': h, 'accepted': False})
        return redirect(url_for('declined'))
   return render_template('index.html', client_ip=client_ip)


@app.route("/form", methods=['GET', 'POST'])
def form():
    # Get client's IP addr
    client_ip = request.remote_addr
    if request.method == 'POST':
        data = request.form['data']
        # Update database
        h = get_hash()
        clients.insert_one({'ip': client_ip, 'data':data})
        return redirect(url_for('form'))
    all_data = clients.find()
    return render_template('form.html', client_ip=client_ip, clients=all_data)

@app.route("/declined", methods=['GET', 'POST'])
def declined(): 
   return render_template('declined.html')

# Delete record
@app.post("/<id>/delete/")
def delete(id):
   clients.delete_one({"_id":ObjectId(id)})
   return redirect(url_for('form'))
    
@app.post("/delete_hash/")
def delete_hash():
   clients.delete_one({"ip_hash": get_hash()})
   return redirect(url_for('index'))

@app.post("/accept/")
def accept():
   update = { "$set": { 'accepted': True } }
   clients.update_one({"ip_hash": get_hash()}, update)
   return redirect(url_for('form'))


# Run web-server
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5050, debug=True)


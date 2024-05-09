from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
import hashlib

############## Initialization ##############
app = Flask(__name__)
client = MongoClient('localhost', 27017)
# Mongodb database
db = client.flask_database
# Collection
clients = db.clients

######## Collection columns ########
# _id
# client_id
# status
# data
# ip_hash
######## Collection columns ########

############## Initialization ##############

@app.route("/", methods=['GET', 'POST'])
def index():
    # Get client's IP addr
    client_ip = request.remote_addr
    # IP Hash
    ip_hash = hashlib.sha256(client_ip.encode()).hexdigest()
    # Check if Client data exist
    client_data = ip_hash_exists(ip_hash)

    if request.method == 'POST':
        data = request.form.get('data')
        action = request.form.get('action', 'decline')

        if client_data:
            # If client data exists, update or delete
            database_update(action, ip_hash, data)
            return redirect(url_for('index'))
        else:
            # Update database
            database_create(data, action, client_ip, ip_hash)
            return redirect(url_for('index'))
    all_data = clients.find()
    return render_template('index.html', client_ip=client_ip, clients=all_data, client_data=client_data)

# Func to create record in database
def database_create(data, action, client_ip, ip_hash):
    # Get a value for client_id
    client_id = get_next_client_id()
    if action == 'accept':
        clients.insert_one({
            'client_id': client_id,
            'ip': client_ip, 
            'status': action,
            'data': data,
            'ip_hash': ip_hash 
            })
        return redirect(url_for('index'))
    elif action == 'decline':
        clients.insert_one({
            'client_id': client_id,
            'status': action,
            'ip_hash': ip_hash
            })
        return redirect(url_for('index'))
    
# Func to update or delete record in database
def database_update(action, ip_hash, data):
    if action == "update":
        update_result = clients.update_one(
            {'ip_hash': ip_hash},
            {'$set': {'data': data}}
        )
        if update_result.modified_count > 0:
            print("Client data updated successfully.")
        return redirect(url_for('index'))
    elif action == "delete":
        clients.delete_one({"ip_hash": ip_hash})

def ip_hash_exists(ip_hash):
    # Check if the client data already exist and return it
    client_data = clients.find_one({'ip_hash': ip_hash})
    return client_data

# Delete record
@app.post("/<id>/delete/")
def delete(id):
    clients.delete_one({"_id":ObjectId(id)})
    return redirect(url_for('index'))

# Create counter collection for set unique client ID
def get_next_client_id():
    result = db.counters.find_one_and_update(
        {'_id': 'client_id'},
        {'$inc': {'seq': 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return result['seq']

# Run web-server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


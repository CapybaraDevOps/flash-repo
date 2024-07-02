from flask import Flask, jsonify, request, session, redirect
from web import clients as db
from web import redis_client
from datetime import datetime
import uuid
import hashlib


class Client:

    def start_session(self, client):
        session['identify'] = True
        session['client'] = client
        # Save client session to Redis DB
        redis_client.set('client', str( session['client']))
        if client['status'] == 'declined':
            return redirect('/client/decline/dashboard/')
        if 'name' in client:
            return True
        return redirect('/client/updatedata/')
    
    def sesion_update(self):
        session['client'] = db.find_one({'_id': session['client']['_id'] })
        # Update client session in Redis DB
        redis_client.set('client', str(session['client']))
        
    def fetch_data(self):
        require_fields = {'name': 1, 'data': 1, 'time': 1, '_id': 0}
        data_db = list(db.find({}, require_fields))
        return data_db

    def delete_record(self, id):
        db.delete_one({'_id': id})
        session.clear()
        redis_client.delete('client')
        return redirect('/')
from flask import Flask, jsonify, request, session, redirect, render_template
from passlib.hash import pbkdf2_sha256
from web import users as db_users
from web import services as db_services
from bson import ObjectId
import uuid

class Service:
    def create_service(self):
        #Create the service object
        service = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "serviceaddress": request.form.get('serviceaddress'),
            "permission": request.form.get('permission'),
            "enabled": request.form.get('enabled', 'off')
        }
        # Check for existing service
        if db_services.find_one({ 
            "$or": [
                {"name": request.form.get('name')},
                {"serviceaddress": request.form.get('serviceaddress')}
                ] 
            }):
            return jsonify({ "error": "Service already in use" }), 400

        # Add Service to db
        if db_services.insert_one(service):
            return jsonify(service), 200
        return jsonify({ "error": "Service creation failed" }), 400
    
    def get_service(self):
        service = db_services.find_one({ 
            "$or": [
                {"name": request.form.get('name')},
                {"serviceaddress": request.form.get('serviceaddress')}
                ] 
            })
        if (service):
            return jsonify(service), 200
        
        return jsonify({ "error": "Invalid service data"}), 401
    
    def fetch_services(self):
        return list(db_services.find())
    
    def update_service(self, service):
        update_fields = {
        "name": request.form.get('name'),
        "serviceaddress": request.form.get('serviceaddress'),
        "permission": request.form.get('permission'),
        "enabled": request.form.get('enabled', 'off')
    }
        new_service = db_services.update_one(
            {'_id': service['_id']},
            {'$set': update_fields}
        )
        updated_service = db_services.find_one({'_id': service['_id']})
        if (updated_service):
            return jsonify(updated_service), 200
        return jsonify({ "error": "Service update failed"}), 400

    def delete_service(self, id):
        db_services.delete_one({'_id': id})
        return redirect('/user/dashboard/admin/')
    
    def delete_service_all(self):
        if session['user']['administrator'] == True:
            db_services.delete_many({})
            return redirect('/user/dashboard/admin/')
        else:
            return jsonify({ "error": "Admin permission required"}), 401
 
from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from web import users as db_users
from web import services as db_services
import uuid

class Service:
    def create_service(self):
        #Create the service object
        service = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "serviceaddress": request.form.get('serviceaddress'),
            "permission": request.form.get('permission'),
            "enabled": True
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
    
    def update_service(self, service):
        new_service = db_services.update_one(
            {'_id': service['_id']},
            {'name': service['name']},
            {'serviceaddress': service['serviceaddress']},
            {'permission': service['permission']},
            {'enabled': service['enabled']},
        )
        if (new_service):
            return jsonify(new_service), 200
        return jsonify({ "error": "Service update failed"}), 400

    def delete_service(self, id):
        db_services.delete_one({'_id': id})
        return redirect('/user/dashboard/admin/')

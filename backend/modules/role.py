from flask import Flask, jsonify, request, session, redirect
import uuid
from web import role as db_role

class Role:
    def create_role(self):
        #Create the role object
        role = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "permission": request.form.get('permissions_list'),
        }
        # Check for existing Role
        if db_role.find_one({ 
            "$or": [
                {"name": request.form.get('name')},
                ] 
            }):
            return jsonify({ "error": "Role already exists" }), 400

        # Add Role to db
        if db_role.insert_one(role):
            return jsonify(role), 200
        return jsonify({ "error": "Role creation failed" }), 400
    
    def fetch_roles(self):
        return list(db_role.find())
    
    def update_role(self, role):
        update_fields = {
        "name": request.form.get('name'),
        "permission": request.form.get('permissions_list'),
    }
        new_role = db_role.update_one(
            {'_id': role['_id']},
            {'$set': update_fields}
        )
        updated_role = db_role.find_one({'_id': role['_id']})
        if (updated_role):
            return jsonify(updated_role), 200
        return jsonify({ "error": "Role update failed"}), 400

    def delete_role(self, id):
        db_role.delete_one({'_id': id})
        return redirect('/user/dashboard/admin/')
    
    def delete_role_all(self):
        if session['user']['administrator'] == True:
            db_role.delete_many({})
            return redirect('/user/dashboard/admin/')
        else:
            return jsonify({ "error": "Admin permission required"}), 401
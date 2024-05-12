from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from web import users as db
import uuid

class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):

        #Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # Check for existing email address
        if db.find_one({ 
            "$or": [
                {"name": request.form.get('name')},
                {"email": request.form.get('email')}
                ] 
            }):
            return jsonify({ "error": "Email/Username address already in use" }), 400

        # Add User to db
        if db.insert_one(user):
            return self.start_session(user)

        return jsonify({ "error": "Singup failed" }), 400
    
    def signout(self):
        session.clear()
        return redirect('/')
    
    def login(self):
        user = db.find_one({
            "$or": [
                {"name": request.form.get('name')},
                {"email": request.form.get('name')}
            ]
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        
        return jsonify({ "error": "Invalid login credentials"}), 401
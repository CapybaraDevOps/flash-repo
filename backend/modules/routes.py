from flask import Flask, request, render_template
from web import app
from modules.user import User, UserAdmin
from modules.client import Client
from modules.service import Service
from modules.role import Role
from web import services as db_services
from web import role as db_role

############ Users Route ############

@app.route('/user/signup', methods=['POST'])
def sign_up():
  return User().signup()

@app.route('/user/signout')
def sign_out():
  return User().signout()

@app.route('/user/login', methods=['POST'])
def log_in():
  return User().login()

@app.route('/user/admin/update_roles/<id>', methods=['GET', 'POST'])
def roles_update(id):
  return UserAdmin().update_roles(id)

@app.route('/user/admin/delete/<id>')
def admin_delete_record(id):
  return UserAdmin().delete_record(id)

@app.route('/user/admin/delete_all')
def admin_delete_record_all():
  return UserAdmin().delete_record_all()

@app.route('/user/admin/users_all')
def users_records_all():
  return UserAdmin().fetch_data()

############ Clients Route ############

@app.route('/client/delete/<id>')
def client_delete(id):
  return Client().delete_record(id)

############ Service Route ############

@app.route('/user/admin/service_create', methods=['POST'])
def service_create():
  return Service().create_service()

@app.route('/user/admin/service_update/<id>', methods=['GET', 'POST'])
def service_update(id):
  service = db_services.find_one({'_id': id})
  return Service().update_service(service)

@app.route('/user/admin/delete_service/<id>')
def service_delete(id):
  return Service().delete_service(id)

@app.route('/user/admin/delete_service_all')
def delete_all_service():
  return Service().delete_service_all()

############ Role Route ############

@app.route('/user/admin/role_create', methods=['POST'])
def role_create():
  return Role().create_role()

@app.route('/user/admin/role_update/<id>', methods=['GET', 'POST'])
def role_update(id):
  role = db_role.find_one({'_id': id})
  return Role().update_role(role)

@app.route('/user/admin/delete_role/<id>')
def role_delete(id):
  return Role().delete_role(id)

@app.route('/user/admin/delete_role_all')
def delete_all_role():
  return Role().delete_role_all()
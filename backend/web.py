from flask import Flask, render_template, session, redirect, request
from pymongo import MongoClient
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.middleware.proxy_fix import ProxyFix
from functools import wraps
import os
import redis

############## Initialization ##############

app = Flask(__name__)

app.secret_key = b'\x9d\x18\x8bH`\x03\xae\x00\xf3L\xd3\xaf\x06\xc8\x9a\x92'
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Map variables
for variable, value in os.environ.items():
    if variable.startswith("MONGO_"):
        env_name = variable.split("MONGO_")[1]
        app.config[env_name] = value
        print(env_name)

# Local DB for Development
# client = MongoClient('localhost', 27017)

# Connect to Mongo
client = MongoClient('mongodb', username=app.config['USER'], password=app.config['PASSWORD'], authSource='flask_database', authMechanism='SCRAM-SHA-256')

# Initialize Redis client
redis_client = redis.Redis(host='redis', port=6379, charset="utf-8", decode_responses=True, db=0)

# Database
db = client.flask_database

# Collection
users = db.users
clients = db.clients
services = db.services
role = db.role

############## Swagger ##############
SWAGGER_URL = '/docs'  # URL route for Swagger UI
API_URL = '/static/swagger.json'  # Our API url (local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "MongoDB Flask App"
    },
)
app.register_blueprint(swaggerui_blueprint)


############## Decorators ##############
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwardgs):
        if 'logged_in' in session:
            return f(*args, **kwardgs)
        else:
            return redirect('/')
    return wrap

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwardgs):
        if session['user']["administrator"] == True:
            return redirect('/user/dashboard/admin/')
        else:
            return f(*args, **kwardgs)
    return wrap

def identify_required(f):
    @wraps(f)
    def wrap(*args, **kwardgs):
        if 'identify' in session:
            return f(*args, **kwardgs)
        else:
            return redirect('/')
    return wrap

############## Modules ##############
from modules import routes
from modules.client import Client
from modules.user import UserAdmin
from modules.service import Service
from modules.role import Role

# Create Admin acount
UserAdmin().signup(name=app.config['ADMIN_USER'], email=app.config['ADMIN_EMAIL'], password=app.config['ADMIN_PASS'])

@app.route('/')
def home():
    service_data = Service().fetch_services()
    return render_template('home.html', service_data=service_data)

############## Users HTML ##############

@app.route('/user/dashboard/')
@admin_required
def dashboard():
    data_db = Client().fetch_data()
    service_data = Service().fetch_services()
    return render_template('user/dashboard.html', data_db=data_db, service_data=service_data)

@app.route('/user/dashboard/admin/')
@login_required
def client_dashboard_admin():
    data_db = UserAdmin().fetch_data()
    service_data = Service().fetch_services()
    role_data = Role().fetch_roles()
    return render_template('user/dashboard_admin.html', data_db=data_db, service_data=service_data, role_data=role_data)

@app.route('/user/login/')
def login():
    return render_template('user/login.html')

@app.route('/user/registry/')
def registry():
    return render_template('user/registry.html')

@app.route('/user/admin/roleupdate/<id>')
def user_role_update(id):
    role_data = Role().fetch_roles()
    return render_template('user/role_update.html', id=id, role_data=role_data)

############## Services HTML ##############

@app.route('/user/admin/serviceupdate/<id>')
def service_update_data(id):
    return render_template('service/service_update.html', id=id)

############## Roles HTML ##############

@app.route('/user/admin/rolesupdate/<id>')
def roles_update_data(id):
    return render_template('role/update_role.html', id=id)
from flask import Blueprint, request, jsonify
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# from forex_python.converter import CurrencyCodes
from app.constants.constants import CONSTANTS
from app.extensions import flask_bcrypt, db
from app.models.user_and_workspace import User
from app.account.helpers import get_all_user_workspaces, get_all_invites, get_workspace_settings
from app.account.salt import generate_salt

account = Blueprint('account', __name__)

CHARACTERS_NOT_ALLOWED_IN_EMAIL = CONSTANTS["CHARACTERS_NOT_ALLOWED_IN_EMAIL"]

# In this file: routes concerning signup, login, and user account management

# SIGN UP
@account.route("/register", methods=["POST"])
def register_user():
    # Request requirements: send email (of user), name (of user), and password (of user) in the body
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]

    if name == '' or name == None or len(name) > 200:
        return jsonify({'response':'no name or name not valid'})
    if email == '' or email == None or len(email) > 320 or "@" not in email or any(char in email for char in CHARACTERS_NOT_ALLOWED_IN_EMAIL):
        return jsonify({'response':'no email or email not valid'})
    if password == '' or password == None or len(password) > 60 or len(password) < 6:
        return jsonify({'response':'no password or password not valid'})
    
    user_exists = User.query.filter_by(_email=email).first() is not None

    if user_exists:
        return jsonify({'response':'user already exists'}), 409
    
    salt = generate_salt()
    salted_password = salt + password

    #create user
    try:
        hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode('utf-8')
        new_user = User(name=name, email=email, password=hashed_password, salt=salt)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({'response': 'There was an error registering user', 'error': str(e)}), 500

    access_token = create_access_token(identity=email, expires_delta=timedelta(days=30))
    invites_data = get_all_invites(email)

    response_data ={
        'response':'success', 
        'access_token':access_token,
        'user': {'name': new_user.name, 'email': new_user.email},
        'has_workspaces': False,
        'has_invites': invites_data['has_invites'],
        'invites': invites_data['invites'],
    }
    return jsonify(response_data)

# LOG IN
@account.route("/login", methods=["POST"])
def login():
    # Request requirements: send email (of user), and password (of user) in the body
    email = request.json["email"]
    password = request.json["password"]

    if email == '' or email == None or len(email) > 320 or "@" not in email or any(char in email for char in CHARACTERS_NOT_ALLOWED_IN_EMAIL):
        return jsonify({'response':'no email or invalid email'})
    if password == '' or password == None or len(password) > 60 or len(password) < 6:
        return jsonify({'response':'no password or invalid password'})
    
    user = User.query.filter_by(_email=email).first()
    
    if user is None:
        return jsonify({'response':'unauthorized'}), 401
    
    salted_password = user.salt + password
    
    if not flask_bcrypt.check_password_hash(user.password, salted_password):
        return jsonify({'response':'unauthorized'}), 401
    
    access_token = create_access_token(identity=email, expires_delta=timedelta(days=30))

    workspaces_data = get_all_user_workspaces(email)
    invites_data = get_all_invites(email)

    if user.favorite_workspace_id is not None:
        favorite_workspace_settings = get_workspace_settings(user.favorite_workspace_id)
    else:
        favorite_workspace_settings = ""

    response_data ={
        'response':'Logged in successfully', 
        'access_token':access_token,
        'user': {'name': user.name, 'email': user.email},
        'has_invites': invites_data['has_invites'],
        'invites': invites_data['invites'],
        'has_workspaces': workspaces_data['has_workspaces'],
        'workspaces': workspaces_data['workspaces'],
        'favorite_workspace': workspaces_data['favorite_workspace'],
        'favorite_workspace_settings': favorite_workspace_settings,
    }

    return jsonify(response_data)

@account.route("/delete", methods=["POST"])
@jwt_required()
def delete_user():
    # Request requirements: 'Bearer token' in request header 
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404

    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        return jsonify({'response': 'There was an error deleting the user', 'error': str(e)}), 500

    return jsonify({'response': 'User deleted successfully'})

@account.route("/change_user", methods=["POST"]) # TEST ROUTE
@jwt_required() 
def change_user():
    # Request requirements: 'Bearer token' in request header and the following in the body:
    # name (of user)
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404

    name = request.json["name"]
    if name == '' or name == None or len(name) > 200:
        return jsonify({'response':'no name or name not valid'})

    try:
        user.name = name
        db.session.commit()
    except Exception as e:
        return jsonify({'response': 'There was an error changing the user', 'error': str(e)}), 500

    return jsonify({'response': 'User changed successfully'})


# The following account-related implementations are missing: reset password and change email.
# Also, sending email functionality in some functions (marked in capital-letter comments)
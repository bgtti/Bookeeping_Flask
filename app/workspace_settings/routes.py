from flask import Blueprint, request, jsonify
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import jsonschema
# from forex_python.converter import CurrencyCodes
from app.extensions import flask_bcrypt, db
from app.models.user_workspace import User, Workspace
from app.models.workspace_settings_general import Group, Account
from schemas import general_json_schema

workspace_settings = Blueprint('workspace_settings', __name__)

# IN THIS FILE: routes used to set, modify and delete Workspace Settings

CHARACTERS_NOT_ALLOWED = ["<",">","/","\\", "--"]

# General settings: Group and Account

# @workspace_settings.route("/add_group", methods=["POST"])# TEST ROUTE
# @jwt_required()  
# def add_group():
#     # Request requirements: 'Bearer token' in request header and the following in the body:
#     # workspace_uuid, name, description, code
#     current_user_email = get_jwt_identity()
#     user = User.query.filter_by(_email=current_user_email).first()
#     if not user:
#         return jsonify({'response': 'User not found'}), 404
    
#     # Check if workspace exists and if user is either owner or has access to it
#     workspace_uuid = request.json.get("workspace_uuid")
#     workspace = Workspace.query.filter_by(_uuid=workspace_uuid).first()

#     if not workspace:
#         return jsonify({'response': 'Workspace not found'}), 404

#     if workspace.owner_id != user.id or not workspace.users.filter_by(id=user.id).first():
#         return jsonify({'response': 'You do not have access to this workspace'}), 403
    
#     # Check if Group information is correct
#     name = request.json.get("name")

#     if name == '' or name == None or len(name) > 30 or any(char in name for char in CHARACTERS_NOT_ALLOWED):
#         return jsonify({'response':'no name or name not valid'}, 400)
    
#     description = request.json.get("description")

#     if description and description != None and description != "":
#         if  len(description) > 100 or any(char in description for char in CHARACTERS_NOT_ALLOWED):
#             return jsonify({'response':'description not valid'}, 400)

#     code = request.json.get("code")

#     if code and code != None and code != "":
#         if  len(code) > 10 or any(char in code for char in CHARACTERS_NOT_ALLOWED):
#             return jsonify({'response':'code not valid'}, 400)

#     # Sve group
#     try:
#         new_group = Group(name=name, description=description, code=code, workspace_id=workspace.id)
#         db.session.add(new_group)
#         db.session.commit()
#     except Exception as e:
#         return jsonify({'response': 'There was an error adding group', 'error': str(e)}), 500

#     print("group success")
#     return jsonify({'response': 'Group added successfully'})

@workspace_settings.route("/add_group", methods=["POST"])
@jwt_required()
def add_group():
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Validate the JSON data against the schema
    try:
        jsonschema.validate(instance=json_data, schema=general_json_schema)
    except jsonschema.exceptions.ValidationError as e:
        # Handle validation errors
        return jsonify({'response': 'Invalid JSON data', 'error': str(e)}), 400

    # Request requirements: 'Bearer token' in request header and the following in the body:
    # workspace_uuid, name, description, code
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404
    
    # Check if workspace exists and if user is either owner or has access to it
    workspace_uuid = json_data.get("workspace_uuid")
    workspace = Workspace.query.filter_by(_uuid=workspace_uuid).first()

    if not workspace:
        return jsonify({'response': 'Workspace not found'}), 404

    if workspace.owner_id != user.id or not workspace.users.filter_by(id=user.id).first():
        return jsonify({'response': 'You do not have access to this workspace'}), 403

    # Save group
    try:
        new_group = Group(name=json_data["name"], description=json_data.get("description"), code=json_data.get("code"), workspace_id=workspace.id)
        db.session.add(new_group)
        db.session.commit()
    except Exception as e:
        return jsonify({'response': 'There was an error adding group', 'error': str(e)}), 500

    print("group success")
    return jsonify({'response': 'Group added successfully'})

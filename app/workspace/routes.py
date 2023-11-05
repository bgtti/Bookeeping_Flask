from flask import Blueprint, request, jsonify
from datetime import timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity
# from forex_python.converter import CurrencyCodes
from app.extensions import db
from app.models.user_and_workspace import User, Workspace
from app.models.invite import Invite, INVITE_TYPES
from app.account.helpers import get_all_user_workspaces, get_workspace_settings
from app.workspace.helpers import checkIfCurrencyInList 

workspace = Blueprint('workspace', __name__)

# TO-DO: favorite workspace & routes related to sharing a workspace have not been tested
# this is to be implemented after other features

@workspace.route("/add_workspace", methods=["POST"])
@jwt_required() 
def add_workspace():
    # Request requirements: 'Bearer token' in request header and add in body:
    # name (of workspace), currency (of workspace), abbreviation, and whether is_favorite is True or False
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404

    # Check if user reached 10 owned Workspace limit
    if len(user.owned_workspaces) >= 10:
        return jsonify({'response': 'You have reached the maximum number of owned workspaces'}), 400
    
    # Check if user already has a favorite workspace. If not, add this one as favorite
    has_favorite = user.favorite_workspace_id 
    if has_favorite is None:
        is_favorite = True
    else:
        is_favorite = False

    name = request.json.get("name")
    currency = request.json.get("currency")
    abbreviation = request.json.get("abbreviation")
    #is_favorite = "False" # when accepting is_favorite: request.json.get("is_primary")

    if not name or name == "" or len(name) > 50:
        return jsonify({'response': 'Invalid name'}), 400
    
    if not checkIfCurrencyInList(currency):
        return jsonify({'response': 'Invalid currency'}), 400
    
    if not abbreviation or abbreviation == "" or len(abbreviation) > 2:
        return jsonify({'response': 'Invalid abbreviation'}), 400

    # Create and add the workspace
    try:
        new_workspace = Workspace(name=name, abbreviation=abbreviation, owner_id=user.id, currency=currency)
        db.session.add(new_workspace)
        db.session.commit()
    except Exception as e:
        return jsonify({'response': 'There was an error adding the workspace', 'error': str(e)}), 500

    if is_favorite:
        # add Workspace id to user as favorite
        try:
            user.favorite_workspace_id  = new_workspace.id
            db.session.commit()
        except Exception as e:
            return jsonify({'response': 'Workspace added, but could not make favorite', 'error': str(e)}), 500
        
    workspaces_data = get_all_user_workspaces(user.email)
    favorite_workspace_settings = get_workspace_settings(user.favorite_workspace_id)

    response_data ={
        'response':'Workspace added successfully', 
        'has_workspaces': workspaces_data['has_workspaces'],
        'favorite_workspace': workspaces_data['favorite_workspace'],
        'workspaces': workspaces_data['workspaces'],
        'favorite_workspace_settings': favorite_workspace_settings,
    }

    return jsonify(response_data)

@workspace.route("/delete_workspace", methods=["POST"])
@jwt_required()
def delete_workspace():
    # Request requirements: 'Bearer token' in request header and the following in the body:
    # workspace_uuid
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404

    workspace_uuid = request.json.get("workspace_uuid")
    if not workspace_uuid:
        return jsonify({'response': 'Workspace UUID not provided'}), 400
    
    workspace = Workspace.query.filter_by(_uuid=workspace_uuid).first()
    if not workspace:
        return jsonify({'response': 'Workspace not found'}), 404
    if workspace.owner_id != user.id:
        return jsonify({'response': 'You are not the owner of this workspace'}), 403

    if user.favorite_workspace_id == workspace.id:
        try:
            user.favorite_workspace_id = None
            db.session.commit()
        except Exception as e:
            return jsonify({'response': 'Could not delete workspace from favorite', 'error': str(e)}), 500
        
    # Check if there are users with access to this workspace and remove access
    users_with_access = workspace.users.all()
    if users_with_access:
        try:
            for user_with_access in users_with_access:
                if user_with_access.favorite_workspace_id == workspace.id:
                    user_with_access.favorite_workspace_id = None
                user_with_access.accessed_workspaces.remove(workspace)
            db.session.commit()
            # SEND EMAIL TO THESE USERS TO INFORM OF WORKSPACE DELETION
        except Exception as e:
            return jsonify({'response': 'There was a problem removing workspace access to some users', 'error': str(e)}), 500
        
    try:
        db.session.delete(workspace)
        db.session.commit()
    except Exception as e:
        return jsonify({'response': 'There was an error deleting workspace', 'error': str(e)}), 500

    workspaces_data = get_all_user_workspaces(user.email)

    response_data ={
        'response':'Workspace deleted successfully', 
        'has_workspaces': workspaces_data['has_workspaces'],
        'favorite_workspace': workspaces_data['favorite_workspace'],
        'workspaces': workspaces_data['workspaces']
    } 
    return jsonify(workspaces_data)

@workspace.route("/edit_workspace", methods=["POST"])
@jwt_required()  
def edit_workspace():
    # Request requirements: 'Bearer token' in request header and the following in the body:
    # name (of workspace), currency (of workspace), abbreviation, and workspace_uuid
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404

    name = request.json.get("name")
    currency = request.json.get("currency")
    abbreviation = request.json.get("abbreviation")

    if not name or name== "" or len(name) > 200:
        return jsonify({'response': 'Invalid name'}), 400
    
    valid_currency = checkIfCurrencyInList(currency)
    if valid_currency == False:
        return jsonify({'response': 'Invalid currency'}), 400
    
    if not abbreviation or abbreviation== "" or len(abbreviation) > 2:
        return jsonify({'response': 'Invalid abbreviation'}), 400
    
    # Check if workspace exists and if user owns workspace
    workspace_uuid = request.json.get("workspace_uuid")

    workspace = Workspace.query.filter_by(_uuid=workspace_uuid).first()

    if not workspace:
        return jsonify({'response': 'Workspace not found'}), 404

    if workspace.owner_id != user.id:
        return jsonify({'response': 'You are not the owner of this workspace'}), 403

    # Change workspace
    workspace.name = name
    workspace.currency = currency
    workspace.abbreviation = abbreviation
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({'response': 'There was an error editting the workspace', 'error': str(e)}), 500

    workspaces_data = get_all_user_workspaces(user.email)

    response_data ={
        'response':'Workspace editted successfully', 
        'has_workspaces': workspaces_data['has_workspaces'],
        'favorite_workspace': workspaces_data['favorite_workspace'],
        'workspaces': workspaces_data['workspaces']
    }
    return jsonify(response_data)

#THE FOLLOWING ROUTE HAS NOT BEEN TESTED NOR IMPLEMENTED IN FE
@workspace.route("/make_workspace_favorite", methods=["POST"])# TEST ROUTE
@jwt_required()  
def make_workspace_favorite():
    # Request requirements: 'Bearer token' in request header and the following in the body:
    # workspace_uuid
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404
    
    # Check if workspace exists and if user is either owner or has access to it
    workspace_uuid = request.json.get("workspace_uuid")
    workspace = Workspace.query.filter_by(_uuid=workspace_uuid).first()

    if not workspace:
        return jsonify({'response': 'Workspace not found'}), 404

    if workspace.owner_id != user.id or not workspace.users.filter_by(id=user.id).first():
        return jsonify({'response': 'You do not have access to this workspace'}), 403

    # Make workspace favorite
    try:
        user.favorite_workspace_id = workspace.id
        db.session.commit()
    except Exception as e:
        return jsonify({'response': 'There was an error making the workspace a favorite', 'error': str(e)}), 500

    return jsonify({'response': 'Workspace marked as favorite successfully'})
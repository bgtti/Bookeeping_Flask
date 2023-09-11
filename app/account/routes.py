from flask import Blueprint, request, jsonify
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# from forex_python.converter import CurrencyCodes
from app.extensions import flask_bcrypt, db
from app.models.user_workspace import User, Workspace
from app.models.invite import Invite, INVITE_TYPES
from app.account.helpers import get_all_user_workspaces, get_all_invites, checkIfCurrencyInList

account = Blueprint('account', __name__)

CHARACTERS_NOT_ALLOWED_IN_EMAIL = ["<",">","/","\\", "--"]

# In this file: routes concerning signup, login, account management and workspace management

# TO-DO: favorite workspace & routes related to sharing a workspace have not been tested
# this is to be implemented after other features

@account.route("/register", methods=["POST"])
def register_user():
    # Request requirements: send email (of user), name (of user), and password (of user) in the body
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]

    if name == '' or name == None or len(name) > 200:
        return jsonify({'response':'no name or name not valid'})
    if email == '' or email == None or len(email) > 345 or "@" not in email or any(char in email for char in CHARACTERS_NOT_ALLOWED_IN_EMAIL):
        return jsonify({'response':'no email or email not valid'})
    if password == '' or password == None or len(password) > 70:
        return jsonify({'response':'no password or password not valid'})
    
    user_exists = User.query.filter_by(_email=email).first() is not None

    if user_exists:
        return jsonify({'response':'user already exists'}), 409

    #create user
    try:
        hashed_password = flask_bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name=name, email=email, password=hashed_password)
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

@account.route("/login", methods=["POST"])
def login():
    # Request requirements: send email (of user), and password (of user) in the body
    email = request.json["email"]
    password = request.json["password"]

    if email == '' or email == None or len(email) > 345:
        return jsonify({'response':'no email'})
    if password == '' or password == None or len(password) > 70:
        return jsonify({'response':'no password'})
    
    user = User.query.filter_by(_email=email).first()
    
    if user is None:
        return jsonify({'response':'unauthorized'}), 401
    
    if not flask_bcrypt.check_password_hash(user.password, password):
        return jsonify({'response':'unauthorized'}), 401
    
    access_token = create_access_token(identity=email, expires_delta=timedelta(days=30))

    workspaces_data = get_all_user_workspaces(email)
    invites_data = get_all_invites(email)

    response_data ={
        'response':'success', 
        'access_token':access_token,
        'user': {'name': user.name, 'email': user.email},
        'has_invites': invites_data['has_invites'],
        'invites': invites_data['invites'],
        'has_workspaces': workspaces_data['has_workspaces'],
        'favorite_workspace': workspaces_data['favorite_workspace'],
        'workspaces': workspaces_data['workspaces']
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

@account.route("/add_workspace", methods=["POST"])
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

    name = request.json.get("name")
    currency = request.json.get("currency")
    abbreviation = request.json.get("abbreviation")
    is_favorite = "False" # when accepting is_favorite: request.json.get("is_primary")

    if not name or name == "" or len(name) > 50:
        return jsonify({'response': 'Invalid name'}), 400
    
    valid_currency = checkIfCurrencyInList(currency)
    if valid_currency == False:
        return jsonify({'response': 'Invalid currency'}), 400
    # currencies = CurrencyCodes()
    # if not currencies.get_currency_name(currency):
    #     return jsonify({'response': 'Invalid currency'}), 400
    
    if not abbreviation or abbreviation== "" or len(abbreviation) > 2:
        return jsonify({'response': 'Invalid abbreviation'}), 400

    # Create and add the workspace
    try:
        new_workspace = Workspace(name=name, abbreviation=abbreviation, owner_id=user.id, currency=currency)
        db.session.add(new_workspace)
        db.session.commit()
    except Exception as e:
        return jsonify({'response': 'There was an error adding the workspace', 'error': str(e)}), 500

    if is_favorite == "True":
        # add Workspace id to user as favorite
        try:
            user.favorite_workspace_id = new_workspace.id
            db.session.commit()
        except Exception as e:
            return jsonify({'response': 'Worspace added, but could not make favorite', 'error': str(e)}), 500
        
    workspaces_data = get_all_user_workspaces(user.email)

    response_data ={
        'response':'Workspace added successfully', 
        'has_workspaces': workspaces_data['has_workspaces'],
        'favorite_workspace': workspaces_data['favorite_workspace'],
        'workspaces': workspaces_data['workspaces']
    }

    return jsonify(response_data)

@account.route("/delete_workspace", methods=["POST"])
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

    # if user.favorite_workspace_id == workspace.id:
    #     try:
    #         user.favorite_workspace_id = None
    #         db.session.commit()
    #     except Exception as e:
    #         return jsonify({'response': 'Could not delete workspace from favorite', 'error': str(e)}), 500
        
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

@account.route("/edit_workspace", methods=["POST"])
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
@account.route("/make_workspace_favorite", methods=["POST"])# TEST ROUTE
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


#THE FOLLOWING ROUTE HAS NOT BEEN TESTED NOR IMPLEMENTED IN FE
@account.route("/new_invite", methods=["POST"])
@jwt_required()
def workspace_invite():
    # Request requirements: 'Bearer token' in request header and the following in the body:
    # workspace_uuid, invite_type, invite_title, invite_text, email_of_invited
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404

    workspace_uuid = request.json.get("workspace_uuid")
    invite_type = request.json.get("invite_type")
    invite_title = request.json.get("invite_title")
    invite_text = request.json.get("invite_text")
    email_of_invited = request.json.get("email_of_invited")

    if not workspace_uuid or workspace_uuid == "":
        return jsonify({'response': 'Workspace UUID not provided'}), 400
    if not invite_type or invite_type not in INVITE_TYPES:
        return jsonify({'response': 'Invite type invalid'}), 400
    if not email_of_invited or email_of_invited  == '' or len(email_of_invited ) > 345 or "@" not in email_of_invited  or any(char in email_of_invited  for char in CHARACTERS_NOT_ALLOWED_IN_EMAIL):
        return jsonify({'response':'no email or email of invited not valid'})
    
    workspace = Workspace.query.filter_by(_uuid=workspace_uuid).first()

    if not workspace:
        return jsonify({'response': 'Workspace not found'}), 404

    if workspace.owner_id != user.id:
        return jsonify({'response': 'You are not the owner of this workspace'}), 403
    
    # check for other ownership invitations
    if invite_type == INVITE_TYPES[1]:
        if Invite.query.filter_by(_user_who_sent_invite=user.id, _workflow_in_question=workspace.id,_type=invite_type ).first() is not None:
            return jsonify({'response': 'Ownership change invite already exists and is pending.'}), 409
    if invite_type == INVITE_TYPES[0]:
        if Invite.query.filter_by(_user_who_sent_invite=user.id, _workflow_in_question=workspace.id,_type=invite_type, _email_of_invited=email_of_invited ).first() is not None:
            return jsonify({'response': 'Access invite already exists and is pending.'}), 409

    if not invite_title or invite_title == "":
        invite_title = f"{user.name} has sent you an invitation!"
    
    if not invite_text or invite_text == "":
        if invite_type == INVITE_TYPES[0]:
            invite_text = f"{user.name} has invited you to join {workspace.name}. Click the link to accept!"
        if invite_type == INVITE_TYPES[1]:
            invite_text = f"{user.name} wants to give you ownership of {workspace.name}. Click the link to accept!"

    try:
        new_invite = Invite(type=invite_type, title=invite_title, text=invite_text, email_of_invited=email_of_invited, 
                            user_who_sent_invite=user.id,workspace_in_question = workspace.id)
        db.session.add(new_invite)
        db.session.commit()
    except Exception as e:
        return jsonify({'response': 'There was an error adding invite to the database', 'error': str(e)}), 500
    
    # SEND INVITATION PER EMAIL

    return jsonify({'response': 'Invite sent successfully'})

#THE FOLLOWING ROUTE HAS NOT BEEN TESTED NOR IMPLEMENTED IN FE
@account.route("/remove_access_to_workspace", methods=["POST"]) 
@jwt_required()
def remove_access_to_workspace():
    # Request requirements: 'Bearer token' in request header and the following in the body:
    # workspace_uuid, email_of_user_to_remove
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404

    workspace_uuid = request.json.get("workspace_uuid")
    workspace = Workspace.query.filter_by(_uuid=workspace_uuid).first()
    if not workspace:
        return jsonify({'response': 'Workspace not found'}), 404
    if workspace.owner_id != user.id:
        return jsonify({'response': 'You are not the owner of this workspace'}), 403
    
    email_of_user_to_remove = request.json.get("email_of_user_to_remove")
    user_to_remove = User.query.filter_by(_email=email_of_user_to_remove).first()
    if not user_to_remove:
        return jsonify({'response': 'User to remove not found'}), 404
    
    # Check if the workspace is accessed by the user_to_remove
    if not workspace.users.filter_by(id=user_to_remove.id).first():
        return jsonify({'response': 'User does not have access to this workspace'}), 400

    # Remove workspace access for the user_to_remove
    try:
        workspace.users.remove(user_to_remove)
        db.session.commit()
    except Exception as e:
        return jsonify({'response': 'There was an error removing user access', 'error': str(e)}), 500
    
    # SEND EMAIL TO REMOVED USER INFORMING

    return jsonify({'response': 'Access removed successfully'})


# The following account-related implementations are missing: reset password and change email.
# Also, sending email functionality in some functions (marked in capital-letter comments)
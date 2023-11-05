from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.constants.constants import CONSTANTS
from app.models.user_and_workspace import User, Workspace
from app.models.invite import Invite, INVITE_TYPES

invites = Blueprint('invites', __name__)

CHARACTERS_NOT_ALLOWED_IN_EMAIL = CONSTANTS["CHARACTERS_NOT_ALLOWED_IN_EMAIL"]

# Routes concearning invites and access to workspace 

#THE FOLLOWING ROUTE HAS NOT BEEN TESTED NOR IMPLEMENTED IN FE
@invites.route("/new_invite", methods=["POST"])
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
@invites.route("/remove_access_to_workspace", methods=["POST"]) 
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


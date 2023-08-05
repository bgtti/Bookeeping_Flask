from app.models.user_workspace import User, Workspace
from app.models.invite import Invite, INVITE_TYPES
from app.extensions import db
from app.data.currency_list import currency_list

def get_all_user_workspaces(email):
    """
    requires user's email as input, outputs an object with all workspaces owned by user and shared with user
    """

    # Request requirements: send email (of user), and password (of user) in the body
        
    user = User.query.filter_by(_email=email).first()
    
    all_workspaces_data ={
        'has_workspaces': False,
        'favorite_workspace': None,
        'workspaces': []
    }

    has_owned_workspaces = db.session.query(User).filter_by(id=user.id).join(User.owned_workspaces).first() is not None
    has_accessed_workspaces = db.session.query(User).filter_by(id=user.id).join(User.accessed_workspaces).first() is not None

    # Check if user has workspaces
    if has_owned_workspaces or has_accessed_workspaces:
        # Check if user has favorite workspace
        if user.favorite_workspace and user.favorite_workspace != "" and user.favorite_workspace !=None:
            all_workspaces_data["favorite_workspace"] = {
                "uuid": user.favorite_workspace.uuid,
                "name": user.favorite_workspace.name,
                "currency": user.favorite_workspace.currency,
                "abbreviation": user.favorite_workspace.abbreviation,
            }
        all_workspaces_data["has_workspaces"] = True

        # Add owned workspaces
        for workspace in user.owned_workspaces:
            workspace_data = {
                "uuid": workspace.uuid,
                "name": workspace.name,
                "currency": workspace.currency,
                "abbreviation": workspace.abbreviation,
                "is_owner": True,
                "users_with_access": [],
                "num_users_with_access": 0,
            }

            for user_with_access in workspace.users:
                workspace_data["users_with_access"].append({
                    "name": user_with_access.name,
                    "email": user_with_access.email
                })

            workspace_data["num_users_with_access"] = len(workspace_data["users_with_access"])
            all_workspaces_data["workspaces"].append(workspace_data)

        # Add workspaces with access
        for workspace in user.accessed_workspaces:
            workspace_data = {
                "uuid": workspace.uuid,
                "name": workspace.name,
                "currency": workspace.currency,
                "abbreviation": workspace.abbreviation,
                "is_owner": False,
                "workspace_owner": {
                    "name": workspace.the_owner.name,
                    "email": workspace.the_owner.email
                },
                "users_with_access": [],
                "num_users_with_access": 0,
            }

            for user_with_access in workspace.users:
                workspace_data["users_with_access"].append({
                    "name": user_with_access.name,
                    "email": user_with_access.email
                })

            workspace_data["num_users_with_access"] = len(workspace_data["users_with_access"])
            all_workspaces_data["workspaces"].append(workspace_data)

    return all_workspaces_data

def get_all_invites(email):
    """
    requires user's email as input, outputs an object with all invites data
    """
    all_invites_data ={
        'has_invites': False,
        'invites': []
    }
    # Check if user has invites. If so, send to front end: 
    invites = Invite.query.filter_by(_email_of_invited=email).all()
    if invites:
        all_invites_data["has_invites"] = True
        for invite in invites:
            invite_data = {
                "uuid": invite._uuid,
                "type": invite._type,
                "user_who_sent_invite_name": invite._user_who_sent_invite.name,
                "workspace_in_question_uuid": invite._workspace_in_question.uuid,
            }
            all_invites_data["invites"].append(invite_data)

    return all_invites_data

def checkIfCurrencyInList(currency):
    for currency_info in currency_list:
        if currency_info["code"] == currency:
            return True

    return False
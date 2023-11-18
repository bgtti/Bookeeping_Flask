from app.models.user_and_workspace import User, Workspace
from app.models.invite import Invite
from app.extensions import db

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
        if user.favorite_workspace_id and user.favorite_workspace_id != "" and user.favorite_workspace_id !=None:
            favorite = Workspace.query.filter_by(id=user.favorite_workspace_id).first()
            all_workspaces_data["favorite_workspace"] = {
                "uuid": favorite.uuid,
                "name": favorite.name,
                "currency": favorite.currency,
                "abbreviation": favorite.abbreviation,
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

def get_workspace_settings(workspace_id):
    '''requires workspace id and returns dictionary of workspace settings'''
    workspace = Workspace.query.filter_by(id=workspace_id).first()

    if workspace is None:
        return ""
    
    ws_settings = {
        "uuid": workspace._uuid,
        "groups": [],
        "accounts": [],
        "accounts": [],
        "tags": [],
        "expense_categories": [],
        "expense_numbering_settings": {
            "number_digits": workspace._expense_number_digits,
            "number_format":workspace._expense_number_format,
            "number_start":workspace._expense_number_start,
            "number_year_digits":workspace._expense_number_year_digits,
            "number_separator":workspace._expense_number_separator,
            "number_custom_prefix":workspace._expense_number_custom_prefix,
            "expense_counter":workspace._expense_counter,
            "expense_counter_custom_start": workspace._expense_counter_custom_start
        }
        
    }
    
    # add workspace groups
    the_groups = workspace.get_groups()
    if the_groups:
        for group in the_groups:
            group_data = {
                "uuid": group._uuid,
                "name": group._name,
                "description": group._description,
                "code": group._code,
                "subgroups": [] 
            }
            # Populate subgroup data
            for subgroup in group.subgroups:
                subgroup_info = {
                    "uuid": subgroup.uuid,
                    "name": subgroup.name,
                    "description": subgroup.description,
                    "code": subgroup.code
                }
                group_data["subgroups"].append(subgroup_info)
            ws_settings["groups"].append(group_data)

    # add workspace accounts
    the_accounts = workspace.get_accounts()
    if the_accounts:
        for account in the_accounts:
            account_data = {
                "uuid": account._uuid,
                "name": account._name,
                "description": account._description,
                "code": account._code,
            }
            ws_settings["accounts"].append(account_data)

    # add workspace tags
    the_tags = workspace.get_tags()
    if the_tags:
        for tag in the_tags:
            tag_data = {
                "uuid": tag._uuid,
                "name": tag._name,
                "colour": tag._colour,
            }
            ws_settings["tags"].append(tag_data)
    
    # add expense categories
    the_expense_categories = workspace.get_expense_categories()
    if the_expense_categories:
        for expense_category in the_expense_categories:
            expense_category_data = {
                "uuid": expense_category._uuid,
                "name": expense_category._name,
                "description": expense_category._description,
                "code": expense_category._code,
            }
            ws_settings["expense_categories"].append(expense_category_data)
    
    return ws_settings
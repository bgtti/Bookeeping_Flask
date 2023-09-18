from app.models.user_workspace import User, Workspace
from app.models.invite import Invite, INVITE_TYPES
from app.extensions import db
from app.data.currency_list import currency_list

def get_all_groups(workspace_id):
    '''Requires workspace id and outputs array of all group objects belonging to workspace.'''

    workspace = Workspace.query.filter_by(id=workspace_id).first()

    if not workspace:
        return "Error: workspace could not be found."
    
    groups = workspace.groups

    # Create a list of group data to return
    group_data = []
    for group in groups:
        group_info = {
            "uuid": group.uuid,
            "name": group.name,
            "description": group.description,
            "code": group.code,
        }
        group_data.append(group_info)
    
    return group_data
from app.models.user_and_workspace import User, Workspace
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

# "accounts" bellow refer to the objects belonging to the workspace, not the user's accounts
def get_all_accounts(workspace_id):
    '''Requires workspace id and outputs array of all account objects belonging to workspace.'''

    workspace = Workspace.query.filter_by(id=workspace_id).first()

    if not workspace:
        return "Error: workspace could not be found."
    
    accounts = workspace.accounts

    # Create a list of account data to return
    account_data = []
    for account in accounts:
        account_info = {
            "uuid": account.uuid,
            "name": account.name,
            "description": account.description,
            "code": account.code,
        }
        account_data.append(account_info)
    
    return account_data

def get_all_expense_categories(workspace_id):
    '''Requires workspace id and outputs array of all expence category objects belonging to workspace.'''

    workspace = Workspace.query.filter_by(id=workspace_id).first()

    if not workspace:
        return "Error: workspace could not be found."
    
    expense_categories = workspace.expense_categories

    # Create a list of expense category data to return
    expense_category_data = []
    for category in expense_categories:
        category_info = {
            "uuid": category.uuid,
            "name": category.name,
            "description": category.description,
            "code": category.code,
        }
        expense_category_data.append(category_info)
    
    return expense_category_data
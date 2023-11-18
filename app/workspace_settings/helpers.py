from app.models.user_and_workspace import User, Workspace
from app.models.workspace_group import Group
# from app.models.invite import Invite, INVITE_TYPES
from app.extensions import db
from sqlalchemy.orm import joinedload
# from app.constants.currency_list import currency_list
# def get_all_workspace_settings(workspace_id):
#     '''Requires workspace id and outputs all workspace settings as a dictionary of objects.'''
#     workspace = Workspace.query.filter_by(id=workspace_id).first()

#     if not workspace:
#         return "Error: workspace could not be found."
    
#     # Groups
#     groups = workspace.groups

#     # Create a list of group data to return
#     group_data = []
#     for group in groups:
#         group_info = {
#             "uuid": group.uuid,
#             "name": group.name,
#             "description": group.description,
#             "code": group.code,
#         }
#         group_data.append(group_info)
    
#     # Accounts
#     accounts = workspace.accounts

#     # Create a list of account data to return
#     account_data = []
#     for account in accounts:
#         account_info = {
#             "uuid": account.uuid,
#             "name": account.name,
#             "description": account.description,
#             "code": account.code,
#         }
#         account_data.append(account_info)
    
#     # Categories
#     expense_categories = workspace.expense_categories

#     # Create a list of expense category data to return
#     expense_category_data = []
#     for category in expense_categories:
#         category_info = {
#             "uuid": category.uuid,
#             "name": category.name,
#             "description": category.description,
#             "code": category.code,
#         }
#         expense_category_data.append(category_info)

#     # Numbering format
#     expense_numbering_settings = {
#         "expense_number_digits": workspace._expense_number_digits,
#         "expense_number_format": workspace._expense_number_format,
#         "expense_number_start": workspace._expense_number_start,
#         "expense_number_year_digits": workspace._expense_number_year_digits,
#         "expense_number_separator": workspace._expense_number_separator,
#         "expense_number_custom_prefix": workspace._expense_number_custom_prefix,
#     }
    
#     all_workspace_settings = {
#         "groups": group_data,
#         "accounts":account_data,
#         "expense_categories":expense_category_data,
#         "expense_numbering_settings": expense_numbering_settings
#     }
    
#     return all_workspace_settings

# def get_all_groups(workspace_id):
#     '''Requires workspace id and outputs array of all group objects belonging to workspace, including subgroups.'''

#     workspace = Workspace.query.filter_by(id=workspace_id).first()

#     if not workspace:
#         return "Error: workspace could not be found."

#     # Use a single query to fetch both groups and their subgroups
#     groups = Group.query.filter_by(workspace_id=workspace_id).options(joinedload(Group.subgroups)).all()

#     # Create a list of group data to return
#     group_data = []
#     for group in groups:
#         group_info = {
#             "uuid": group.uuid,
#             "name": group.name,
#             "description": group.description,
#             "code": group.code,
#             "subgroups": []  # Initialize an empty list for subgroups
#         }

#         # Populate subgroup data
#         for subgroup in group.subgroups:
#             subgroup_info = {
#                 "uuid": subgroup.uuid,
#                 "name": subgroup.name,
#                 "description": subgroup.description,
#                 "code": subgroup.code
#             }
#             group_info["subgroups"].append(subgroup_info)

#         group_data.append(group_info)

#     return group_data

def get_all_groups(workspace_id):
    '''Requires workspace id and outputs array of all group objects belonging to workspace, including subgroups.'''
    workspace = Workspace.query.filter_by(id=workspace_id).first()
    groups = workspace.groups
    if not groups:
        return "Error: workspace could not be found."
    # Create a list of group data to return
    group_data = []
    for group in groups:
        group_info = {
            "uuid": group.uuid,
            "name": group.name,
            "description": group.description,
            "code": group.code,
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
            group_info["subgroups"].append(subgroup_info)

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

def get_all_tags(workspace_id):
    '''Requires workspace id and outputs array of all tag objects belonging to workspace.'''

    workspace = Workspace.query.filter_by(id=workspace_id).first()

    if not workspace:
        return "Error: workspace could not be found."
    
    tags = workspace.tags

    # Create a list of tag data to return
    tag_data = []
    for tag in tags:
        tag_info = {
            "uuid": tag.uuid,
            "name": tag.name,
            "colour": tag.colour,
        }
        tag_data.append(tag_info)
    
    return tag_data

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

def get_expense_numbering_settings(workspace_id):
    '''Requires workspace id and outputs a dictionary of numbering settings belonging to workspace.'''

    workspace = Workspace.query.filter_by(id=workspace_id).first()

    if not workspace:
        return "Error: workspace could not be found."
    
    expense_numbering_settings = {
        "number_digits": workspace._expense_number_digits,
        "number_format":workspace._expense_number_format,
        "number_start":workspace._expense_number_start,
        "number_year_digits":workspace._expense_number_year_digits,
        "number_separator":workspace._expense_number_separator,
        "number_custom_prefix":workspace._expense_number_custom_prefix,
        "expense_counter":workspace._expense_counter,
        "expense_counter_custom_start": workspace._expense_counter_custom_start
    }
    
    return expense_numbering_settings


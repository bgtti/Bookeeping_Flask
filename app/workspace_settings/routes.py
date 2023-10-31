from flask import Blueprint, request, jsonify
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import jsonschema
# from forex_python.converter import CurrencyCodes
from app.extensions import flask_bcrypt, db
from app.models.user_and_workspace import User, Workspace
from app.models.workspace_group import Group
from app.models.workspace_account import Account
from app.models.expense_category import Expense_Category
from app.workspace_settings.schemas import add_group_schema, edit_group_schema, delete_group_schema, add_account_schema, edit_account_schema, delete_account_schema, add_expense_category_schema, edit_expense_category_schema, delete_expense_category_schema
from app.workspace_settings.helpers import get_all_groups, get_all_accounts, get_all_expense_categories

workspace_settings = Blueprint('workspace_settings', __name__)

# IN THIS FILE: routes used to set, modify and delete objects in Workspace Settings

CHARACTERS_NOT_ALLOWED = ["<",">","/","\\", "--"]

# General settings: Group, Account, Category, Expense numbering format

@workspace_settings.route("/add_group", methods=["POST"])
@jwt_required()
def add_group():
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Validate the JSON data against the schema
    try:
        jsonschema.validate(instance=json_data, schema=add_group_schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({'response': 'Invalid JSON data.', 'error': str(e)}), 400

    # Validate user and token
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404
    
    # Check if workspace exists and if user is either owner or has access to it
    workspace_uuid = json_data.get("workspace_uuid")
    workspace = Workspace.query.filter_by(_uuid=workspace_uuid).first()
    if not workspace:
        return jsonify({'response': 'Workspace not found.'}), 404
    if workspace.owner_id != user.id or workspace.users.filter_by(id=user.id).first() is not None:
        return jsonify({'response': 'You do not have access to this workspace.'}), 403

    # Save group
    try:
        new_group = Group(name=json_data["name"], description=json_data.get("description"), code=json_data.get("code"), workspace_id=workspace.id)
        db.session.add(new_group)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'response': 'There was an error adding group', 'error': str(e)}), 500
    
    # Get all groups belonging to this WS
    try:
        group_data = get_all_groups(workspace.id)
    except Exception as e:
        return jsonify({'response': 'Group added, but database error prevented group data to be sent.', 'error': str(e)}), 500

    return jsonify(group_data)

@workspace_settings.route("/edit_group", methods=["POST"])
@jwt_required()
def edit_group():
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Validate the JSON data against the schema
    try:
        jsonschema.validate(instance=json_data, schema=edit_group_schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({'response': 'Invalid JSON data.', 'error': str(e)}), 400

    # Validate user and token
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404
    
    # Check if group exists and if user is either owner or has access to it
    group_uuid = json_data["group_uuid"]
    group = Group.query.filter_by(_uuid=group_uuid).first()
    if not group:
        return jsonify({'response': 'Group not found.'}), 404
    if group.workspace.owner_id != user.id or group.workspace.users.filter_by(id=user.id).first() is not None:
        return jsonify({'response': 'You do not have access to this workspace.'}), 403

    # Save group
    # Update group information
    try:
        if "name" in json_data:
            group._name = json_data["name"]
        if "description" in json_data:
            group._description = json_data["description"]
        if "code" in json_data:
            group._code = json_data["code"]
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'response': 'There was an error editing the group', 'error': str(e)}), 500
    
    # Get all groups belonging to this WS
    try:
        group_data = get_all_groups(group.workspace.id)
        
    except Exception as e:
        return jsonify({'response': 'Group added, but database error prevented group data to be sent.', 'error': str(e)}), 500

    return jsonify(group_data)

@workspace_settings.route("/delete_group", methods=["DELETE"])
@jwt_required()
def delete_group():
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Validate the JSON data against the schema
    try:
        jsonschema.validate(instance=json_data, schema=delete_group_schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({'response': 'Invalid JSON data.', 'error': str(e)}), 400

    # Validate user and token
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404

    group_uuid = json_data["group_uuid"]

    # Check if group exists and if user is either the owner or has access to it
    group = Group.query.filter_by(_uuid=group_uuid).first()
    if not group:
        return jsonify({'response': 'Group not found.'}), 404

    # Check if the user is the owner of the workspace that contains the group
    if group.workspace.owner_id != user.id:
        return jsonify({'response': 'You do not have permission to delete this group.'}), 403

    try:
        # Delete the group
        db.session.delete(group)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'response': 'There was an error deleting the group', 'error': str(e)}), 500

    # Get all groups belonging to the workspace after deletion
    try:
        group_data = get_all_groups(group.workspace.id)
    except Exception as e:
        return jsonify({'response': 'Group deleted, but database error prevented group data from being sent.', 'error': str(e)}), 500

    return jsonify(group_data)

# ********** ACCOUNTS *********
# 'account' here refers to the object belonging to the WS, not the user's account

@workspace_settings.route("/add_account", methods=["POST"])
@jwt_required()
def add_account():
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Validate the JSON data against the schema
    try:
        jsonschema.validate(instance=json_data, schema=add_account_schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({'response': 'Invalid JSON data.', 'error': str(e)}), 400

    # Validate user and token
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404
    
    # Check if workspace exists and if user is either owner or has access to it
    workspace_uuid = json_data.get("workspace_uuid")
    workspace = Workspace.query.filter_by(_uuid=workspace_uuid).first()
    if not workspace:
        return jsonify({'response': 'Workspace not found.'}), 404
    if workspace.owner_id != user.id or workspace.users.filter_by(id=user.id).first() is not None:
        return jsonify({'response': 'You do not have access to this workspace.'}), 403

    # Save account
    try:
        new_account = Account(name=json_data["name"], description=json_data.get("description"), code=json_data.get("code"), workspace_id=workspace.id)
        db.session.add(new_account)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'response': 'There was an error adding account', 'error': str(e)}), 500
    
    # Get all accounts belonging to this WS
    try:
        account_data = get_all_accounts(workspace.id)
    except Exception as e:
        return jsonify({'response': 'Account added, but database error prevented account data to be sent.', 'error': str(e)}), 500

    return jsonify(account_data)

@workspace_settings.route("/edit_account", methods=["POST"])
@jwt_required()
def edit_account():
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Validate the JSON data against the schema
    try:
        jsonschema.validate(instance=json_data, schema=edit_account_schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({'response': 'Invalid JSON data.', 'error': str(e)}), 400

    # Validate user and token
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404
    
    # Check if account exists and if user is either owner or has access to it
    account_uuid = json_data["account_uuid"]
    account = Account.query.filter_by(_uuid=account_uuid).first()
    if not account:
        return jsonify({'response': 'Account not found.'}), 404
    if account.workspace.owner_id != user.id or account.workspace.users.filter_by(id=user.id).first() is not None:
        return jsonify({'response': 'You do not have access to this workspace.'}), 403

    # Save account
    # Update account information
    try:
        if "name" in json_data:
            account._name = json_data["name"]
        if "description" in json_data:
            account._description = json_data["description"]
        if "code" in json_data:
            account._code = json_data["code"]
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'response': 'There was an error editing the account', 'error': str(e)}), 500
    
    # Get all accounts belonging to this WS
    try:
        account_data = get_all_accounts(account.workspace.id)
        
    except Exception as e:
        return jsonify({'response': 'Account added, but database error prevented account data to be sent.', 'error': str(e)}), 500

    return jsonify(account_data)

@workspace_settings.route("/delete_account", methods=["DELETE"])
@jwt_required()
def delete_account():
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Validate the JSON data against the schema
    try:
        jsonschema.validate(instance=json_data, schema=delete_account_schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({'response': 'Invalid JSON data.', 'error': str(e)}), 400

    # Validate user and token
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404

    account_uuid = json_data["account_uuid"]

    # Check if account exists and if user is either the owner or has access to it
    account = Account.query.filter_by(_uuid=account_uuid).first()
    if not account:
        return jsonify({'response': 'Account not found.'}), 404

    # Check if the user is the owner of the workspace that contains the account
    if account.workspace.owner_id != user.id:
        return jsonify({'response': 'You do not have permission to delete this account.'}), 403

    try:
        # Delete the account
        db.session.delete(account)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'response': 'There was an error deleting the account', 'error': str(e)}), 500

    # Get all accounts belonging to the workspace after deletion
    try:
        account_data = get_all_accounts(account.workspace.id)
    except Exception as e:
        return jsonify({'response': 'Account deleted, but database error prevented account data from being sent.', 'error': str(e)}), 500

    return jsonify(account_data)

# ********** EXPENSE CATEGORY *********

# Add expense category
@workspace_settings.route("/add_expense_category", methods=["POST"])
@jwt_required()
def add_expense_category():
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Validate the JSON data against the schema
    try:
        jsonschema.validate(instance=json_data, schema=add_expense_category_schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({'response': 'Invalid JSON data.', 'error': str(e)}), 400

    # Validate user and token
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404
    
    # Check if workspace exists and if user is either owner or has access to it
    workspace_uuid = json_data.get("workspace_uuid")
    workspace = Workspace.query.filter_by(_uuid=workspace_uuid).first()
    if not workspace:
        return jsonify({'response': 'Workspace not found.'}), 404
    if workspace.owner_id != user.id or workspace.users.filter_by(id=user.id).first() is not None:
        return jsonify({'response': 'You do not have access to this workspace.'}), 403

    # Save expense category
    try:
        new_expense_category = Expense_Category(name=json_data["name"], description=json_data.get("description"), code=json_data.get("code"), workspace_id=workspace.id)
        db.session.add(new_expense_category)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'response': 'There was an error adding expense category', 'error': str(e)}), 500
    
    # Get all expense categories belonging to this WS
    try:
        expense_category_data = get_all_expense_categories(workspace.id)
    except Exception as e:
        return jsonify({'response': 'Expense category added, but database error prevented expense category data to be sent.', 'error': str(e)}), 500

    return jsonify(expense_category_data)

@workspace_settings.route("/edit_expense_category", methods=["POST"])
@jwt_required()
def edit_expense_category():
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Validate the JSON data against the schema
    try:
        jsonschema.validate(instance=json_data, schema=edit_expense_category_schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({'response': 'Invalid JSON data.', 'error': str(e)}), 400

    # Validate user and token
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404
    
    # Check if expense category exists and if user is either owner or has access to it
    expense_category_uuid = json_data["expense_category_uuid"]
    expense_category = Expense_Category.query.filter_by(_uuid=expense_category_uuid).first()
    if not expense_category:
        return jsonify({'response': 'Expense category not found.'}), 404
    if expense_category.workspace.owner_id != user.id or expense_category.workspace.users.filter_by(id=user.id).first() is not None:
        return jsonify({'response': 'You do not have access to this workspace.'}), 403

    # Save account
    # Update account information
    try:
        if "name" in json_data:
            expense_category._name = json_data["name"]
        if "description" in json_data:
            expense_category._description = json_data["description"]
        if "code" in json_data:
            expense_category._code = json_data["code"]
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'response': 'There was an error editing the expense category', 'error': str(e)}), 500
    
    # Get all expense categories belonging to this WS
    try:
        expense_category_data = get_all_expense_categories(expense_category.workspace.id)
        
    except Exception as e:
        return jsonify({'response': 'Account added, but database error prevented expense category data to be sent.', 'error': str(e)}), 500

    return jsonify(expense_category_data)

@workspace_settings.route("/delete_expense_category", methods=["DELETE"])
@jwt_required()
def delete_expense_category():
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Validate the JSON data against the schema
    try:
        jsonschema.validate(instance=json_data, schema=delete_expense_category_schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({'response': 'Invalid JSON data.', 'error': str(e)}), 400

    # Validate user and token
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404

    expense_category_uuid = json_data["expense_category_uuid"]

    # Check if expense category exists and if user is either the owner or has access to it
    expense_category = Expense_Category.query.filter_by(_uuid=expense_category_uuid).first()
    if not expense_category:
        return jsonify({'response': 'Expense category not found.'}), 404

    # Check if the user is the owner of the workspace that contains the expense category
    if expense_category.workspace.owner_id != user.id:
        return jsonify({'response': 'You do not have permission to delete this expense category.'}), 403

    try:
        # Delete the expense category
        db.session.delete(expense_category)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'response': 'There was an error deleting the expense category', 'error': str(e)}), 500

    # Get all expense categories belonging to the workspace after deletion
    try:
        expense_category_data = get_all_expense_categories(expense_category.workspace.id)
    except Exception as e:
        return jsonify({'response': 'Expense category deleted, but database error prevented expense category data from being sent.', 'error': str(e)}), 500

    return jsonify(expense_category_data)

# ********** EXPENSE NUMBERING *********

# DB expense numbering changes made. Now finish Change expense numbering route.

# Change expense numbering
@workspace_settings.route("/set_expense_numbering_format", methods=["POST"])
@jwt_required()
def set_expense_numbering_format():
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Validate the JSON data against the schema
    try:
        jsonschema.validate(instance=json_data, schema=set_expense_numbering_format_schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({'response': 'Invalid JSON data.', 'error': str(e)}), 400

    # Validate user and token
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(_email=current_user_email).first()
    if not user:
        return jsonify({'response': 'User not found'}), 404
    
    # Check if workspace exists and if user is either owner or has access to it
    workspace_uuid = json_data.get("workspace_uuid")
    workspace = Workspace.query.filter_by(_uuid=workspace_uuid).first()
    if not workspace:
        return jsonify({'response': 'Workspace not found.'}), 404
    if workspace.owner_id != user.id or workspace.users.filter_by(id=user.id).first() is not None:
        return jsonify({'response': 'You do not have access to this workspace.'}), 403

    # Save expense category
    try:
        new_expense_category = Expense_Category(name=json_data["name"], description=json_data.get("description"), code=json_data.get("code"), workspace_id=workspace.id)
        db.session.add(new_expense_category)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'response': 'There was an error adding expense category', 'error': str(e)}), 500
    
    # Get all expense categories belonging to this WS
    try:
        expense_category_data = get_all_expense_categories(workspace.id)
    except Exception as e:
        return jsonify({'response': 'Expense category added, but database error prevented expense category data to be sent.', 'error': str(e)}), 500

    return jsonify(expense_category_data)
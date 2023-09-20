# JSON schemas for instance validation pertaining to Workspace Settings APIs

# Request requirements: 'Bearer token' in request header and the following in the body:

add_group_schema = {
    "type": "object",
    "properties": {
        "workspace_uuid": {"type": "string"},
        "name": {"type": "string", "minLength": 1, "maxLength": 30},
        "description": {"type": "string", "maxLength": 100},
        "code": {"type": "string", "maxLength": 10},
    },
    "required": ["workspace_uuid", "name"]
}

edit_group_schema = {
    "type": "object",
    "properties": {
        "group_uuid": {"type": "string"},
        "name": {"type": "string", "minLength": 1, "maxLength": 30},
        "description": {"type": "string", "maxLength": 100},
        "code": {"type": "string", "maxLength": 10},
    },
    "required": ["group_uuid", "name"]
}

delete_group_schema = {
    "type": "object",
    "properties": {
        "group_uuid": {"type": "string"}
    },
    "required": ["group_uuid"]
}

# account bellow refers to the object belonging to the WS, not the user's account
add_account_schema = {
    "type": "object",
    "properties": {
        "workspace_uuid": {"type": "string"},
        "name": {"type": "string", "minLength": 1, "maxLength": 30},
        "description": {"type": "string", "maxLength": 100},
        "code": {"type": "string", "maxLength": 10},
    },
    "required": ["workspace_uuid", "name"]
}

edit_account_schema = {
    "type": "object",
    "properties": {
        "account_uuid": {"type": "string"},
        "name": {"type": "string", "minLength": 1, "maxLength": 30},
        "description": {"type": "string", "maxLength": 100},
        "code": {"type": "string", "maxLength": 10},
    },
    "required": ["account_uuid", "name"]
}

delete_account_schema = {
    "type": "object",
    "properties": {
        "account_uuid": {"type": "string"}
    },
    "required": ["account_uuid"]
}
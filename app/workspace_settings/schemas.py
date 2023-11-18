# JSON schemas for instance validation pertaining to Workspace Settings APIs
# Request requirements: 'Bearer token' in request header and the following in the body accordinngly

all_workspace_settings_schema = {
    "type": "object",
    "properties": {
        "workspace_uuid": {"type": "string"},
    },
    "additionalProperties": False,
    "required": ["workspace_uuid"]
}

# GROUPS
add_group_schema = {
    "type": "object",
    "properties": {
        "workspace_uuid": {"type": "string"},
        "name": {"type": "string", "minLength": 1, "maxLength": 30},
        "description": {"type": "string", "maxLength": 100},
        "code": {"type": "string", "maxLength": 10},
    },
    "additionalProperties": False,
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
    "additionalProperties": False,
    "required": ["group_uuid", "name"]
}

delete_group_schema = {
    "type": "object",
    "properties": {
        "group_uuid": {"type": "string"}
    },
    "additionalProperties": False,
    "required": ["group_uuid"]
}

# SUBGROUPS
add_subgroup_schema = {
    "type": "object",
    "properties": {
        "group_uuid": {"type": "string"},
        "name": {"type": "string", "minLength": 1, "maxLength": 30},
        "description": {"type": "string", "maxLength": 100},
        "code": {"type": "string", "maxLength": 10},
    },
    "additionalProperties": False,
    "required": ["group_uuid", "name"]
}

edit_subgroup_schema = {
    "type": "object",
    "properties": {
        "group_uuid": {"type": "string"},
        "subgroup_uuid": {"type": "string"},
        "name": {"type": "string", "minLength": 1, "maxLength": 30},
        "description": {"type": "string", "maxLength": 100},
        "code": {"type": "string", "maxLength": 10},
    },
    "additionalProperties": False,
    "required": ["subgroup_uuid", "name"]
}
delete_subgroup_schema = {
    "type": "object",
    "properties": {
        "subgroup_uuid": {"type": "string"}
    },
    "additionalProperties": False,
    "required": ["subgroup_uuid"]
}

# ACCOUNTS
# account bellow refers to the object belonging to the WS, not the user's account
add_account_schema = {
    "type": "object",
    "properties": {
        "workspace_uuid": {"type": "string"},
        "name": {"type": "string", "minLength": 1, "maxLength": 30},
        "description": {"type": "string", "maxLength": 100},
        "code": {"type": "string", "maxLength": 10},
    },
    "additionalProperties": False,
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
    "additionalProperties": False,
    "required": ["account_uuid", "name"]
}

delete_account_schema = {
    "type": "object",
    "properties": {
        "account_uuid": {"type": "string"}
    },
    "additionalProperties": False,
    "required": ["account_uuid"]
}

# TAGS
add_tag_schema = {
    "type": "object",
    "properties": {
        "workspace_uuid": {"type": "string"},
        "name": {"type": "string", "minLength": 1, "maxLength": 30},
        "colour": {"type": "string", "minLength": 7, "maxLength": 7},
    },
    "additionalProperties": False,
    "required": ["workspace_uuid", "name"]
}

edit_tag_schema = {
    "type": "object",
    "properties": {
        "tag_uuid": {"type": "string"},
        "name": {"type": "string", "minLength": 1, "maxLength": 30},
        "colour": {"type": "string", "minLength": 7, "maxLength": 7},
    },
    "additionalProperties": False,
    "required": ["tag_uuid", "name"]
}

delete_tag_schema = {
    "type": "object",
    "properties": {
        "tag_uuid": {"type": "string"}
    },
    "additionalProperties": False,
    "required": ["tag_uuid"]
}

# EXPENSE CATEGORY
add_expense_category_schema = {
    "type": "object",
    "properties": {
        "workspace_uuid": {"type": "string"},
        "name": {"type": "string", "minLength": 1, "maxLength": 30},
        "description": {"type": "string", "maxLength": 100},
        "code": {"type": "string", "maxLength": 10},
    },
    "additionalProperties": False,
    "required": ["workspace_uuid", "name"]
}

edit_expense_category_schema = {
    "type": "object",
    "properties": {
        "expense_category_uuid": {"type": "string"},
        "name": {"type": "string", "minLength": 1, "maxLength": 30},
        "description": {"type": "string", "maxLength": 100},
        "code": {"type": "string", "maxLength": 10},
    },
    "additionalProperties": False,
    "required": ["expense_category_uuid", "name"]
}

delete_expense_category_schema = {
    "type": "object",
    "properties": {
        "expense_category_uuid": {"type": "string"}
    },
    "additionalProperties": False,
    "required": ["expense_category_uuid"]
}

# EXPENSE NUMBERING
set_expense_numbering_format_schema = {
    "type": "object",
    "properties": {
        "workspace_uuid": {"type": "string"},
        "expense_number_digits": {"type": "integer", "minimum": 3, "maximum": 5},
        "expense_number_format": {"type": "string", "minLength": 1, "maxLength": 3},
        "expense_number_start": {"type": "integer", "minimum": 1, "maximum": 999999999999},
        "expense_number_year_digits": {"type": "integer", "minimum": 2, "maximum": 4,  "multipleOf" : 2},
        "expense_number_separator": {"type": "string", "minLength": 0, "maxLength": 1},
        "expense_number_custom_prefix": {"type": "string", "minLength": 0, "maxLength": 10},
    },
    "additionalProperties": False,
    "minProperties": 7
}

general_json_schema = {
    "type": "object",
    "properties": {
        "workspace_uuid": {"type": "string"},
        "name": {"type": "string", "minLength": 1, "maxLength": 30},
        "description": {"type": "string", "maxLength": 100},
        "code": {"type": "string", "maxLength": 10},
    },
    "required": ["workspace_uuid", "name"]
}
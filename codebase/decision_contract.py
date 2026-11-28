"""Decision vocabulary shared by the model request and backend validation."""
ALLOWED_ISSUES = {
    "propose": {"missing"},
    "ask": {"unclear"},
    "handoff": {"out_of_scope", "policy"},
    "refuse": {"policy"},
}

DECISION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["action", "issue", "item", "amount"],
    "properties": {
        "action": {"type": "string", "enum": list(ALLOWED_ISSUES)},
        "issue": {"type": "string", "enum": sorted(set().union(*ALLOWED_ISSUES.values()))},
        "item": {"type": ["string", "null"]},
        "amount": {"type": ["integer", "null"]},
    },
}

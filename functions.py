from flask import jsonify, request

def toJson(code, message="", results={}):
    return jsonify(dict(code=code, message=message, results=results)), code

def isRequired(required_field={}, data={}):
    message = ""
    missing = False
    for field in required_field:
        if field not in data:
            message += f"Le champs '{field}' est requis."
            missing = True
        elif str(data[field]).strip() == "":
            message += f"Le champs '{field}' ne peut pas être vide."
            missing = True
    if missing:
        return message
    return False
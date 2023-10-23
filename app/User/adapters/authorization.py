from functools import wraps
from flask import request, jsonify
from User.application.use_cases.manage_jwt import CreateJWT
from configuration import configuration

configuration = configuration()
jwt = CreateJWT(configuration)

def is_authorized(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Unauthorized"}), 401
        
        user_info = jwt.validate_access_token(token)

        if not user_info:
            return jsonify({"message": "Unauthorized"}), 401

        # Here, you can check user roles and permissions if needed

        return func(*args, **kwargs)

    return decorated_function

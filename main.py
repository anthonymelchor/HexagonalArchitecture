from crypt import methods
import json
from flask import Flask, request, jsonify
from User.application.use_cases.create_user import CreateUser
from User.application.use_cases.get_users import GetUsers
from User.application.use_cases.validation import Validation 
from User.application.use_cases.login_user import LoginUser
from User.application.use_cases.manage_jwt import CreateJWT
from User.application.use_cases.get_user import GetUSer
from User.application.use_cases.update_user import UpdateUser
from User.adapters.user_adapter import UserAdapter
from configuration import configuration
from User.adapters.authorization import is_authorized


app = Flask(__name__)

configuration = configuration()
sqlalchemy_adapter = UserAdapter(configuration)

use_case_create_user = CreateUser(sqlalchemy_adapter)
use_case_get_users = GetUsers(sqlalchemy_adapter)
use_case_login_user = LoginUser(sqlalchemy_adapter)
validate_email = Validation(sqlalchemy_adapter)
use_case_jwt = CreateJWT(configuration)
use_case_get_user = GetUSer(sqlalchemy_adapter)
use_case_update_user = UpdateUser(sqlalchemy_adapter)

@app.route('/api/v1/users', methods=['POST'])
@is_authorized
def create_user():
    try:
        data = request.get_json()
        name = data["name"]
        role = data["role"]
        email = data["email"]
        password = data["password"]
        avatar = data["avatar"]

        if validate_email.email_exists(email):
            return jsonify({"message":"Email already exists"}), 409

        user = use_case_create_user.create_user(name, role, email, password, avatar)

        if user:
            return jsonify({
                "id":user.id,
                "name": user.name,
                "password": user.password,
                "email": user.email,
                "role": user.role,
                "avatar": user.avatar
            })
        else:
            return jsonify({"Error":"Internal Server Error"}), 500

    except Exception as e:
        return jsonify({'Error':"Internal Server Error"}), 500


@app.route('/api/v1/users', methods=['GET'])
@is_authorized
def get_users():
    try:
        users = use_case_get_users.get_users()
        user_list = []
        for user in users:
            user_data = {
                "id":user.id,
                "name": user.name,
                "password": user.password,
                "email": user.email,
                "role": user.role,
                "avatar": user.avatar
            }
            user_list.append(user_data)
        return jsonify(user_list)
    except Exception as e:
        return jsonify({'Error':"Internal Server Error"}), 500

@app.route('/api/v1/users/<id>', methods=["GET"])
@is_authorized
def get_user(id):
    try:
        id = int(id)
        user = use_case_get_user.get_user(id)
        if user:
            return jsonify({
                "id":user.id,
                "name": user.name,
                "password": user.password,
                "email": user.email,
                "role": user.role,
                "avatar": user.avatar
            })
        else:
            return jsonify({"message":"User not found"}), 404
    except Exception as e:
        return jsonify({"Error":"Internal Server Error"}), 500    

@app.route('/api/v1/users/<id>', methods=["PUT"])
@is_authorized
def update_user(id):
    try:
        data = request.get_json()

        user = use_case_get_user.get_user(id)

        if user is None:
            return jsonify({"message":"User not found"}), 404
        
        if "name" in data:
            user.name = data["name"]
        if "role" in data:
            user.role = data["role"]
        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.password = data["password"]
        if "avatar" in data:
            user.avatar = data["avatar"]
        
        user_data = {
            "name": user.name,
            "password": user.password,
            "email": user.email,
            "role": user.role,
            "avatar": user.avatar
        }

        user = use_case_update_user.update_user(id, user_data)

        if user:
            return jsonify({
                "id":user.id,
                "name": user.name,
                "password": user.password,
                "email": user.email,
                "role": user.role,
                "avatar": user.avatar
            })
        else:
            return jsonify({"Error":"Internal Server Error"}), 500
        
    except Exception as e:
        return jsonify({"Error":e}), 500

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    try: 
        data = request.get_json()
        email = data['email']
        password = data['password']
        user = use_case_login_user.login_user(email, password)
        if user:
            user_info = {
                "id":user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "avatar": user.avatar
            }
            acces_token,refresh_token = use_case_jwt.create_token(user_info)
            return jsonify({"access_token":acces_token, "refresh_token":refresh_token})
        else:
            return jsonify({"message":"Email or password is invalid"}), 401   
    except Exception as e:
        return jsonify({"Error":"Internal Server Error"}), 500

@app.route("/api/v1/auth/refresh-token", methods=["POST"])
def refresh_token():
    data = request.get_json()
    new_acces_token  = use_case_jwt.renew_access_token(data['refreshToken'])
    if new_acces_token:
        return jsonify({"acces_token":new_acces_token, "refresh_token":data['refreshToken']})
    else:
        return jsonify({"message": "Unauthorized"}), 401


@app.route("/api/v1/auth/profile", methods=["POST"])
def get_user_profile():
    
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message":"Unathorized"}), 401
    
    payload = use_case_jwt.get_user_profile(token)

    if not payload:
        return jsonify({"message":"Unathorized"}), 401
    
    user_claim = payload.get("user")

    user_info = {
        "id":user_claim.get("id"),
        "name": user_claim.get("name"),
        "email": user_claim.get("email"),
        "role": user_claim.get("role"),
        "avatar": user_claim.get("avatar")
    }
    return user_info

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)


    
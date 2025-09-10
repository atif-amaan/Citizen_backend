from flask import Blueprint, request, jsonify
from models import user_model
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

user_bp = Blueprint("user", __name__)

@user_bp.route('/users/register', methods=['POST'])
def register_user():
    data = request.json
    # store plain-text password
    user_id = user_model.create_user(data['name'], data['email'], data['password'])
    user = user_model.get_user_by_email(data['email'])
    token = create_access_token(identity={'id': user['id'], 'role': user['role']})
    return jsonify({"message": "User registered ✅", "user": user, "token": token})


@user_bp.route('/users/login', methods=['POST'])
def login_user():
    data = request.json
    user = user_model.get_user_by_email(data['email'])
    
    if user and user['password'] == data['password']:
        token = create_access_token(identity={'id': user['id'], 'role': user['role']})
        return jsonify({"message": "Login success ✅", "user": user, "token": token})
    
    return jsonify({"message": "Invalid credentials ❌"}), 401


@user_bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    return jsonify({"message": "User profile", "user": current_user})

# 🔹 Admin-only route to create departments or other admins
@user_bp.route('/users/create', methods=['POST'])
@jwt_required()
def create_user_by_admin():
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"message": "Unauthorized ❌"}), 403

    data = request.json
    role = data.get("role", "citizen")  # default citizen, but admin can choose "department" or "admin"

    if role not in ["citizen", "department", "admin"]:
        return jsonify({"message": "Invalid role ❌"}), 400

    user_id = user_model.create_user(data['name'], data['email'], data['password'], role)
    return jsonify({"message": f"{role.capitalize()} created ✅", "user_id": user_id})

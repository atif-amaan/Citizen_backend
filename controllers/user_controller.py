from flask import Blueprint, request, jsonify
from models import user_model

user_bp = Blueprint("user", __name__)

@user_bp.route('/users/register', methods=['POST'])
def register_user():
    data = request.json
    user_id = user_model.create_user(data['name'], data['email'], data['password'])
    return jsonify({"message": "User registered ✅", "user_id": user_id})

@user_bp.route('/users/login', methods=['POST'])
def login_user():
    data = request.json
    user = user_model.get_user_by_email(data['email'])
    if user and user['password'] == data['password']:
        return jsonify({"message": "Login success ✅", "user": user})
    return jsonify({"message": "Invalid credentials ❌"}), 401

from flask import Blueprint, request, jsonify
from models import user_model

user_bp = Blueprint("user", __name__)

@user_bp.route('/users/register', methods=['POST'])
def register_user():
    data = request.json
    user_id = user_model.create_user(data['name'], data['email'], data['password'], role="citizen")
    user = user_model.get_user_by_email(data['email'])
    return jsonify({"message": "User registered ✅", "user": user})

@user_bp.route('/users/login', methods=['POST'])
def login_user():
    data = request.json
    user = user_model.get_user_by_email(data['email'])

    if user and user['password'] == data['password']:  # ⚠ plain text (hackathon only)
        return jsonify({"message": "Login success ✅", "user": user})

    return jsonify({"message": "Invalid credentials ❌"}), 401

@user_bp.route('/users/me/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    user = user_model.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"message": "User profile", "user": user})

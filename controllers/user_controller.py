from flask import Blueprint, request, jsonify
from models import user_model
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# bcrypt import removed since we're storing plain-text as requested

user_bp = Blueprint("user", __name__)

@user_bp.route('/users/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        if not data.get("name") or not data.get("email") or not data.get("password"):
            return jsonify({"message": "Missing required fields"}), 400

        user_id = user_model.create_user(data['name'], data['email'], data['password'])
        user = user_model.get_user_by_id(user_id)
        token = create_access_token(
                identity=user['id'],                # only user id
                additional_claims={"role": user['role']}  # role goes here
                )

        return jsonify({"message": "User registered ✅", "user": user, "token": token})
    except Exception as e:
        import traceback
        print("❌ Registration error:", str(e))
        traceback.print_exc()
        return jsonify({"message": "Registration failed", "error": str(e)}), 500



@user_bp.route('/users/login', methods=['POST'])
def login_user():
    data = request.json
    user = user_model.get_user_by_email(data['email'])
    
    # plain-text comparison (per your requirement). Trim spaces to be safe:
    if user and str(user['password']).strip() == str(data['password']).strip():
        token = create_access_token(identity=user['id'])   # identity is scalar user_id
        return jsonify({"message": "Login success ✅", "user": user, "token": token})
    
    return jsonify({"message": "Invalid credentials ❌"}), 401


@user_bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = user_model.get_user_by_id(current_user_id)
    return jsonify({"message": "User profile", "user": user})


# Admin-only route to create users (admin/department)
@user_bp.route('/users/create', methods=['POST'])
@jwt_required()
def create_user_by_admin():
    current_user_id = get_jwt_identity()
    current_user = user_model.get_user_by_id(current_user_id)
    if current_user["role"] != "admin":
        return jsonify({"message": "Unauthorized ❌"}), 403

    data = request.json
    role = data.get("role", "citizen")  # default citizen, admin can choose "department" or "admin"

    if role not in ["citizen", "department", "admin"]:
        return jsonify({"message": "Invalid role ❌"}), 400

    user_id = user_model.create_user(data['name'], data['email'], data['password'], role)
    return jsonify({"message": f"{role.capitalize()} created ✅", "user_id": user_id})

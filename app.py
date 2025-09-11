from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from controllers.user_controller import user_bp
from controllers.report_controller import report_bp

app = Flask(__name__)
CORS(app)

# 🔑 JWT Configuration
app.config["JWT_SECRET_KEY"] = "supersecretkey123"  # change to env var in production
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(report_bp)

@app.route('/')
def home():
    return {"message": "Backend is running"}

# Custom error for missing/invalid JWT
@jwt.unauthorized_loader
def missing_token_callback(err):
    return jsonify({"msg": "Missing Authorization Header"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(err):
    return jsonify({"msg": "Invalid token"}), 422

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

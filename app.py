from flask import Flask
from flask_cors import CORS
from controllers.user_controller import user_bp
from controllers.report_controller import report_bp

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(report_bp)

@app.route('/')
def home():
    return {"message": "Backend is running"}

if __name__ == '__main__':
    app.run(debug=True)

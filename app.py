from flask import Flask, send_from_directory
from controllers.user_controller import user_bp
from controllers.report_controller import report_bp
import os

app = Flask(__name__)

# Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(report_bp)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)


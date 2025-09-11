from flask import Blueprint, request, jsonify
from models import report_model, user_model
import os
from werkzeug.utils import secure_filename

report_bp = Blueprint("report", __name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@report_bp.route('/report', methods=['POST'])
def add_report():
    user_id = request.form.get('user_id')
    user = user_model.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    if user["role"] != "citizen":
        return jsonify({"message": "Only citizens can submit reports"}), 403

    issue_type = request.form.get('issue_type')
    description = request.form.get('description')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    file = request.files.get('image')
    image_url = None
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Get full URL instead of relative path
        image_url = request.host_url.rstrip("/") + "/uploads/" + filename

    report_id = report_model.create_report(user_id, issue_type, description, latitude, longitude, image_url)
    return jsonify({"message": "Report submitted ✅", "report_id": report_id})

@report_bp.route('/reports', methods=['GET'])
def get_reports():
    reports = report_model.get_all_reports()
    return jsonify(reports)

@report_bp.route('/myreports/<int:user_id>', methods=['GET'])
def get_my_reports(user_id):
    reports = report_model.get_reports_by_user(user_id)
    return jsonify(reports)

@report_bp.route('/report/<int:report_id>', methods=['PUT'])
def update_status(report_id):
    status = request.json.get('status')
    report_model.update_report_status(report_id, status)
    return jsonify({"message": "Status updated 🔄"})

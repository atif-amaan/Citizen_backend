from flask import Blueprint, request, jsonify
from models import report_model
import os
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity

report_bp = Blueprint("report", __name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@report_bp.route('/report', methods=['POST'])
@jwt_required()
def add_report():
    current_user = get_jwt_identity()
    if current_user["role"] != "citizen":
        return jsonify({"message": "Only citizens can submit reports"}), 403

    user_id = current_user["id"]
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
        image_url = filepath

    report_id = report_model.create_report(user_id, issue_type, description, latitude, longitude, image_url)
    return jsonify({"message": "Report submitted ✅", "report_id": report_id})

@report_bp.route('/reports', methods=['GET'])
@jwt_required()
def get_reports():
    current_user = get_jwt_identity()
    if current_user["role"] not in ["admin", "department"]:
        return jsonify({"message": "Unauthorized"}), 403

    reports = report_model.get_all_reports()
    return jsonify(reports)

@report_bp.route('/report/<int:report_id>', methods=['PUT'])
@jwt_required()
def update_status(report_id):
    current_user = get_jwt_identity()
    if current_user["role"] not in ["admin", "department"]:
        return jsonify({"message": "Only admins or departments can update status"}), 403

    status = request.json.get('status')
    report_model.update_report_status(report_id, status)
    return jsonify({"message": "Status updated 🔄"})

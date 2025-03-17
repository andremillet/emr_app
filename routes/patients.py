# routes/patients.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.patient import Patient
from models.audit_log import AuditLog
from utils.cpf_validator import is_valid_cpf

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/patients', methods=['GET'])
@jwt_required()
def list_patients():
    user_id = get_jwt_identity()  # Already a string, e.g., "1"
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    filter_name = request.args.get('filter[name]')
    result = Patient.get_paginated(page, limit, filter_name)
    AuditLog.log(user_id, "list_access")
    return jsonify(result), 200

@patients_bp.route('/patients/new', methods=['POST'])
@jwt_required()
def create_patient():
    user_id = get_jwt_identity()  # Already a string, e.g., "1"
    claims = get_jwt()  # Access additional claims
    role = claims['role']
    if role != 'admin':  # Restrict creation to admins
        return jsonify({"error": "Admin access required"}), 403
    
    data = request.get_json()
    required_fields = ['full_name', 'dob', 'gender', 'address', 'phone', 'email', 'cpf']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    if data['gender'] not in ['M', 'F']:
        return jsonify({"error": "Gender must be 'M' or 'F'"}), 400
    
    if not is_valid_cpf(data['cpf']):
        return jsonify({"error": "Invalid CPF"}), 400
    
    try:
        patient = Patient.create(data)
        AuditLog.log(user_id, "patient_create", str(patient['patient_id']))
        return jsonify({"message": "Patient created", "patient": patient}), 201
    except Exception as e:
        if "unique constraint" in str(e):
            return jsonify({"error": "CPF already exists"}), 409
        return jsonify({"error": "Server error"}), 500

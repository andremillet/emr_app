# routes/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.users import User
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400
    
    username = data['username']
    password = data['password']
    
    user = User.get_by_username(username)
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
        return jsonify({"error": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=str(user['user_id']), additional_claims={'role': user['role']})
    return jsonify({"access_token": access_token}), 200

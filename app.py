# emr_app/app.py
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from routes.patients import patients_bp
from routes.auth import auth_bp
from models.patient import Patient
from models.audit_log import AuditLog
from models.users import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['JWT_SECRET_KEY'] = Config.SECRET_KEY
    
    # Enable CORS for local dev and Render frontend
    CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "https://emr-frontend-o4mv.onrender.com", "https://emr-app-4jan.onrender.com"]}})
    
    # Explicit CORS headers as fallback
    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get('Origin')
        allowed_origins = ["http://localhost:3000", "https://emr-frontend-o4mv.onrender.com", "https://emr-app-4jan.onrender.com"]
        if origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        return response
    
    # Handle OPTIONS preflight requests
    @app.route('/login', methods=['OPTIONS'])
    def login_options():
        return jsonify({}), 200
    
    @app.route('/patients', methods=['OPTIONS'])
    def patients_options():
        return jsonify({}), 200
    
    @app.route('/patients/<int:patient_id>', methods=['OPTIONS'])
    def patient_options(patient_id):
        return jsonify({}), 200
    
    @app.route('/patients/new', methods=['OPTIONS'])
    def patients_new_options():
        return jsonify({}), 200
    
    jwt = JWTManager(app)
    
    Patient.create_table()
    AuditLog.create_table()
    User.create_table()
    
    app.register_blueprint(patients_bp)
    app.register_blueprint(auth_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    app = create_app()

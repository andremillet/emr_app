# app.py
from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from routes.patients import patients_bp
from models.patient import Patient
from models.audit_log import AuditLog
from models.users import User
from routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['JWT_SECRET_KEY'] = Config.SECRET_KEY  # Use the secure key from .env
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize DB tables
    Patient.create_table()
    AuditLog.create_table()
    User.create_table()
    
    # Register routes
    app.register_blueprint(patients_bp)
    app.register_blueprint(auth_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

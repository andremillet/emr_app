# app.py
from flask import Flask
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
    
    # Enable CORS for local dev and Render frontend (adjust origins as needed)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "https://<your_frontend_url>.onrender.com"]}})
    
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

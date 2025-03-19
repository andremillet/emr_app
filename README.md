# EMR System Development Roadmap

## Overview
This roadmap tracks the development of an Electronic Medical Record (EMR) system built with Flask (Python), PostgreSQL, and a React frontend, targeting HIPAA compliance for internal staff use at a small clinic. The system replaces manual/paper-based processes, allowing staff to create, view, and manage patient records with role-based access (admins create/edit, clinicians view). It’s deployed on Render.com, with plans for additional features and full compliance. The roadmap is divided into phases, each with tasks, their status, and next steps, so you can always see where you are when you stop.

## Current Status (As of March 20, 2025)
- **Phase**: Additional Features (Phase 7)
- **Progress**: Core backend with authentication, role-based access, security enhancements, and a React frontend are fully deployed and functional. Added /patients/{patient_id} endpoint for viewing/editing patient details, integrated into the frontend.
- **Key Features**:
  - Backend: /patients (GET), /patients/new (POST, admin-only), /patients/{patient_id} (GET, PUT), /login (JWT with bcrypt).
  - Frontend: Login, patient list, admin-only creation form, patient details/edit page.
  - Deployment: Backend at https://emr-app-4jan.onrender.com, frontend at https://emr-frontend-o4mv.onrender.com.
- **Location**: In Phase 7, task 1 (Add /patients/{patient_id}) completed, ready for task 2 (Implement patient search by CPF).

## Development Phases

### Phase 1: Initial Setup and Core Endpoints
- **Goal**: Establish the basic backend structure and core functionality.
- **Tasks**:
  - Set up Flask with PostgreSQL (psycopg).
  - Create /patients (GET) for listing patients.
  - Create /patients/new (POST) for adding patients.
  - Implement manual CPF validation.
  - Set up audit logging for HIPAA compliance.
- **Status**: Completed
- **Details**: 
  - Directory: emr_app/ with app.py, config.py, models/, routes/, utils/.
  - .env: DATABASE_URL and SECRET_KEY configured.
  - Local PostgreSQL running with emr_user.

### Phase 2: Authentication and Role-Based Access
- **Goal**: Secure endpoints with JWT and enforce role restrictions.
- **Tasks**:
  - Add users table and model (SHA-256 hashing initially).
  - Implement /login endpoint with JWT (flask-jwt-extended).
  - Protect /patients and /patients/new with @jwt_required().
  - Restrict /patients/new to admin role using JWT claims.
  - Fix JWT identity issues (string vs. dict).
- **Status**: Completed
- **Details**:
  - Users: admin1 (user_id 1, role admin), clinician1 (user_id 2, role clinician).
  - JWT: user_id as identity, role as claim.

### Phase 3: Role-Based Testing and Validation
- **Goal**: Verify role-based access control works as intended.
- **Tasks**:
  - Add a clinician user (clinician1).
  - Test /patients/new with admin (should succeed).
  - Test /patients/new with clinician (should fail with 403).
  - Test /patients with both roles (should succeed).
  - Verify audit logs reflect correct user_ids and actions.
- **Status**: Completed
- **Details**: Completed role-based testing on March 17, 2025. Admin can create patients, clinician restricted to listing, logs verified with user_ids 1 and 2.

### Phase 4: Security Enhancements
- **Goal**: Strengthen security for HIPAA compliance.
- **Tasks**:
  - Replace SHA-256 with bcrypt for password hashing.
  - Add input validation (e.g., phone, email formats).
  - Implement rate limiting on /login to prevent brute force attacks.
  - Configure PostgreSQL encryption at rest.
- **Status**: Partially Completed
- **Details**: Completed bcrypt hashing and input validation on March 17, 2025. Updated users table to BYTEA, rehashed admin1 and clinician1 with bcrypt, added phone (+55, 2-digit region, 8-9 digits) and email validation, verified all endpoints. Rate limiting and encryption at rest remain for later.

### Phase 5: Deployment to Render.com
- **Goal**: Deploy the app to a cloud platform with HTTPS.
- **Tasks**:
  - Create Render.com account and project.
  - Configure PostgreSQL on Render with encryption at rest.
  - Set up environment variables (DATABASE_URL, SECRET_KEY).
  - Deploy Flask app with HTTPS enabled.
  - Test endpoints in production.
- **Status**: Completed
- **Details**: Deployed to Render.com on March 18, 2025 at https://emr-app-4jan.onrender.com. Configured PostgreSQL (emr_db_e6y7) with internal URL, migrated local data via pg_dump/psql (ignored transaction_timeout warning and default privileges error due to Render restrictions), deployed Flask app with Gunicorn, set HTTPS, tested /login, /patients, /patients/new successfully with admin and clinician roles.

### Phase 6: React Frontend
- **Goal**: Build a user interface for staff to interact with the backend.
- **Tasks**:
  - Set up React project with create-react-app.
  - Create login page to fetch JWT.
  - Build patient list view (/patients).
  - Build patient creation form (/patients/new).
  - Handle role-based UI restrictions (e.g., hide create form for clinicians).
- **Status**: Completed
- **Details**: Completed Phase 6 on March 19, 2025. Set up React project (emr-frontend in emr_app/emr-frontend), added login component with axios, resolved CORS with flask-cors 5.0.0 on backend (redeployed to https://emr-app-4jan.onrender.com), added patient list and admin-only patient creation form with jwt-decode, improved styling, added auto-refresh, fixed build errors (homepage URL, missing public/index.html, removed build directory, adjusted buildCommand and staticPublishPath), deployed to Render at https://emr-frontend-o4mv.onrender.com, tested login, listing, and creation with admin1 and clinician1 (password 123456). Fixed CORS issue on March 20, 2025 by adding explicit CORS headers and OPTIONS routes.

### Phase 7: Additional Features
- **Goal**: Expand functionality and refine the system.
- **Tasks**:
  - Add /patients/{patient_id} (GET, PUT) for details/edit.
  - Implement patient search by cpf.
  - Add logout (token blacklist or short expiration).
  - Write unit tests for endpoints and validation.
  - Document API for frontend team (e.g., OpenAPI spec).
- **Status**: In Progress
- **Details**: Started Phase 7 on March 20, 2025. Added /patients/{patient_id} endpoint for viewing and editing patient details, tested with admin1 via curl, confirmed CORS fix for frontend login, verified endpoint functionality with GET and PUT requests, updated React frontend to include patient details/edit page, tested with admin1, successfully viewed and edited patient details (e.g., Paciente Novo). Added /patients/search endpoint for CPF search, integrated into React frontend, tested with admin1.

### Phase 8: Final HIPAA Compliance and Release
- **Goal**: Ensure full HIPAA compliance and prepare for production use.
- **Tasks**:
  - Audit all endpoints for PHI exposure.
  - Implement data retention policy (e.g., 5 years).
  - Set up secure backups on Render.
  - Conduct security audit (e.g., penetration testing).
  - Release v1.0 with documentation.
- **Status**: Not Started
- **Details**: Planned for future phase after core features are complete.

## Current Location
- **Phase 7: Additional Features**
- **Task in Progress**: Task 2 (Implement patient search by CPF) completed, ready for Task 3 (Add logout functionality).
- **Last Confirmed**: Frontend login works, /patients/{patient_id} endpoint and frontend integration tested successfully with admin1, CPF search implemented and tested on March 20, 2025.



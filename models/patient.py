# emr_app/models/patient.py
from utils.db import get_db_connection

class Patient:
    @staticmethod
    def create_table():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id SERIAL PRIMARY KEY,
                full_name VARCHAR(100) NOT NULL,
                dob DATE NOT NULL,
                gender CHAR(1) NOT NULL CHECK (gender IN ('M', 'F')),
                address TEXT NOT NULL,
                phone VARCHAR(15) NOT NULL,
                email VARCHAR(100) NOT NULL,
                cpf VARCHAR(11) NOT NULL UNIQUE
            );
        """)
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def create(data):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO patients (full_name, dob, gender, address, phone, email, cpf)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING patient_id, full_name, dob, gender, address, phone, email, cpf;
        """, (
            data['full_name'],
            data['dob'],
            data['gender'],
            data['address'],
            data['phone'],
            data['email'],
            data['cpf']
        ))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return dict(zip(['patient_id', 'full_name', 'dob', 'gender', 'address', 'phone', 'email', 'cpf'], result))

    @staticmethod
    def get_paginated(page, limit, filter_name):
        conn = get_db_connection()
        cur = conn.cursor()
        offset = (page - 1) * limit
        query = "SELECT patient_id, full_name, cpf FROM patients"
        params = []
        if filter_name:
            query += " WHERE full_name ILIKE %s"
            params.append(f"%{filter_name}%")
        query += " ORDER BY full_name ASC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        cur.execute(query, params)
        patients = [dict(zip(['patient_id', 'full_name', 'cpf'], row)) for row in cur.fetchall()]
        
        cur.execute("SELECT COUNT(*) FROM patients" + (" WHERE full_name ILIKE %s" if filter_name else ""), 
                    ([f"%{filter_name}%"] if filter_name else []))
        total = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        return {"patients": patients, "total": total, "page": page, "limit": limit}

    @staticmethod
    def get_by_id(patient_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT patient_id, full_name, dob, gender, address, phone, email, cpf
            FROM patients
            WHERE patient_id = %s;
        """, (patient_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result:
            return dict(zip(['patient_id', 'full_name', 'dob', 'gender', 'address', 'phone', 'email', 'cpf'], result))
        return None

    @staticmethod
    def update(patient_id, data):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE patients
            SET full_name = %s, dob = %s, gender = %s, address = %s, phone = %s, email = %s, cpf = %s
            WHERE patient_id = %s
            RETURNING patient_id, full_name, dob, gender, address, phone, email, cpf;
        """, (
            data['full_name'],
            data['dob'],
            data['gender'],
            data['address'],
            data['phone'],
            data['email'],
            data['cpf'],
            patient_id
        ))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if result:
            return dict(zip(['patient_id', 'full_name', 'dob', 'gender', 'address', 'phone', 'email', 'cpf'], result))
        return None

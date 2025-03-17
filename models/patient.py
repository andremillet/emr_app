# models/patient.py
from utils.db import get_db_connection

class Patient:
    @staticmethod
    def create_table():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id SERIAL PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                dob DATE NOT NULL,
                gender CHAR(1) CHECK (gender IN ('M', 'F')) NOT NULL,
                address TEXT NOT NULL,
                phone VARCHAR(20) NOT NULL,
                email VARCHAR(255) NOT NULL,
                cpf VARCHAR(11) UNIQUE NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def create(patient_data):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO patients (full_name, dob, gender, address, phone, email, cpf)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING patient_id, full_name, dob, gender, address, phone, email, cpf;
        """, (
            patient_data['full_name'], patient_data['dob'], patient_data['gender'],
            patient_data['address'], patient_data['phone'], patient_data['email'],
            patient_data['cpf']
        ))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return dict(zip(['patient_id', 'full_name', 'dob', 'gender', 'address', 'phone', 'email', 'cpf'], result))

    @staticmethod
    def get_paginated(page=1, limit=10, filter_name=None):
        conn = get_db_connection()
        cur = conn.cursor()
        offset = (page - 1) * limit
        query = "SELECT patient_id, full_name, cpf FROM patients"
        params = []
        if filter_name:
            query += " WHERE full_name ILIKE %s"
            params.append(f"%{filter_name}%")
        query += " ORDER BY full_name LIMIT %s OFFSET %s;"
        params.extend([limit, offset])
        
        cur.execute(query, params)
        patients = [dict(zip(['patient_id', 'full_name', 'cpf'], row)) for row in cur.fetchall()]
        
        cur.execute("SELECT COUNT(*) FROM patients" + (" WHERE full_name ILIKE %s" if filter_name else ""), 
                   ([f"%{filter_name}%"] if filter_name else []))
        total = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        return {"patients": patients, "total": total, "page": page, "limit": limit}

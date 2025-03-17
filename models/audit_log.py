# models/audit_log.py
from utils.db import get_db_connection

class AuditLog:
    @staticmethod
    def create_table():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(50) NOT NULL,  -- Placeholder, assumes auth later
                action VARCHAR(50) NOT NULL,
                resource_id VARCHAR(50),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def log(user_id, action, resource_id=None):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO audit_logs (user_id, action, resource_id)
            VALUES (%s, %s, %s);
        """, (user_id, action, resource_id))
        conn.commit()
        cur.close()
        conn.close()

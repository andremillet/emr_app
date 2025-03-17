# models/users.py
from utils.db import get_db_connection
import bcrypt

class User:
    @staticmethod
    def create_table():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash BYTEA NOT NULL,  -- Changed to BYTEA for bcrypt binary
                role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'clinician'))
            );
        """)
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def create(username, password, role):
        # Generate salt and hash password with bcrypt
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (username, password_hash, role)
            VALUES (%s, %s, %s)
            RETURNING user_id, username, role;
        """, (username, password_hash, role))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return dict(zip(['user_id', 'username', 'role'], result))

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id, username, password_hash, role FROM users WHERE username = %s;", (username,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result:
            return dict(zip(['user_id', 'username', 'password_hash', 'role'], result))
        return None

# utils/db.py
import psycopg
from config import Config

def get_db_connection():
    try:
        conn = psycopg.connect(Config.DATABASE_URL)
        return conn
    except Exception as e:
        raise Exception(f"Database connection failed: {str(e)}")

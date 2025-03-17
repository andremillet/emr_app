# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file if present

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "d096f341e651fc11163c18e04a25eb9bfb9e731be1289f97513a04d7a664e7b")  # For future auth
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://emr_user:nazarenoam1805@localhost:5432/emr_db")

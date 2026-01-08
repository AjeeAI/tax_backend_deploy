from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import logging
import ssl      # Import SSL
import certifi  # Import Certifi

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- UPDATED ENGINE CONFIGURATION ---
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": certifi.where()  # Keep this for secure connection
        }
    },
    #  ADDED THESE LINES TO FIX THE DISCONNECTION ERROR:
    pool_pre_ping=True,    # Tests the connection before handing it to the app
    pool_recycle=1800,     # Refreshes connections every 30 minutes
    pool_size=10,          # Keeps up to 10 connections ready
    max_overflow=20        # Allows 20 extra temporary connections if busy
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auto-create tables on import
def init_db():
    try:
        from database.models import User
        Base.metadata.create_all(bind=engine)
        logging.info("Database tables created/verified")
    except Exception as e:
        logging.error(f"Failed to create database tables: {e}")
        raise

# Call init_db when this module is imported
init_db()
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ============================================================
# CONEXIÓN A MYSQL
# ============================================================

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

connect_args = {}

# Aiven requiere SSL
if SQLALCHEMY_DATABASE_URL and "aivencloud.com" in SQLALCHEMY_DATABASE_URL:
    connect_args["ssl"] = {"check_hostname": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    """Obtiene una sesión de base de datos para FastAPI."""

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
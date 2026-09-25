from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ============================================================
# CONEXIÓN A MYSQL
# ============================================================

SQLALCHEMY_DATABASE_URL = (
    "mysql+pymysql://root:19741026@localhost/inmobiliaria"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False
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
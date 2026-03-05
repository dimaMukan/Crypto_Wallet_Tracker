from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
import sqlite3

DATABASE_URL = "sqlite:///./wallets.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os

DATABASE_URL = "sqlite:///./site.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}, # Needed for SQLite + FastAPI
    echo=False
)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

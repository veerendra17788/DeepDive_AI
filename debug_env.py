import sys
import os

print(f"Python executable: {sys.executable}")

try:
    print("Importing sqlmodel...", end="")
    from sqlmodel import SQLModel, Session, select, create_engine
    print("OK")
except ImportError as e:
    print(f"FAILED: {e}")
    sys.exit(1)

try:
    print("Importing passlib & bcrypt...", end="")
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hash = pwd_context.hash("test")
    print("OK")
except Exception as e:
    print(f"FAILED: {e}")

try:
    print("Checking Database...", end="")
    DATABASE_URL = "sqlite:///./site.db"
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    print("OK")
    
    print("Attempting DB Write...", end="")
    from models import User
    with Session(engine) as session:
        # Check if we can select
        user = session.exec(select(User).limit(1)).first()
        print("OK (Read)")
except Exception as e:
    print(f"FAILED: {e}")

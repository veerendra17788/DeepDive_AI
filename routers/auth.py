from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta
from database import get_session
from models import User
from auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from typing import Annotated

router = APIRouter(prefix="/auth", tags=["auth"])

import traceback
import sys

@router.post("/register")
async def register(email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    try:
        print(f"Attempting registration for {email}", file=sys.stderr)
        user = session.exec(select(User).where(User.email == email)).first()
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Auto-truncate to 71 characters to be safe (bcrypt limit is 72 bytes)
        safe_password = password[:71]
        hashed_password = get_password_hash(safe_password)
        new_user = User(email=email, password_hash=hashed_password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        print(f"User registered successfully: {new_user.id}", file=sys.stderr)
        return {"message": "User created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Checking error during registration: {e}", file=sys.stderr)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    safe_password_login = form_data.password[:71]
    if not user or not verify_password(safe_password_login, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

import os
import requests as http_requests
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta
from database import get_session
from models import User
from auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from typing import Annotated
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

import traceback
import sys

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")


class GoogleCredential(BaseModel):
    credential: str


@router.post("/register")
async def register(email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    try:
        print(f"Attempting registration for {email}", file=sys.stderr)
        user = session.exec(select(User).where(User.email == email)).first()
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = get_password_hash(password)
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
    if not user or not verify_password(form_data.password, user.password_hash):
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


@router.post("/google")
async def google_auth(body: GoogleCredential, session: Session = Depends(get_session)):
    """
    Verify Google OAuth credential and create/login user.
    Uses Google's tokeninfo endpoint to verify the JWT — no extra library needed.
    """
    try:
        # Verify Google token via Google's API
        resp = http_requests.get(
            "https://oauth2.googleapis.com/tokeninfo",
            params={"id_token": body.credential},
            timeout=5
        )
        
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid Google credential")
        
        google_data = resp.json()
        
        # Verify audience matches our client ID
        if GOOGLE_CLIENT_ID and google_data.get("aud") != GOOGLE_CLIENT_ID:
            raise HTTPException(status_code=401, detail="Token audience mismatch")
        
        email = google_data.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="No email in Google credential")
        
        # Find or create user
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            # Auto-create account for Google users (no password needed)
            new_user = User(email=email, password_hash="GOOGLE_OAUTH_USER")
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            user = new_user
            print(f"Auto-created Google user: {email}", file=sys.stderr)
        
        # Issue JWT
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Google auth error: {e}", file=sys.stderr)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Google authentication failed")


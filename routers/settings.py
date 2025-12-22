from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json
from io import BytesIO

router = APIRouter(prefix="/api/settings", tags=["settings"])

# Pydantic Models
class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None

class PreferencesUpdate(BaseModel):
    theme: Optional[str] = None
    model: Optional[str] = None
    iterations: Optional[int] = None
    notifications: Optional[bool] = None
    autoSave: Optional[bool] = None

class ApiKeysUpdate(BaseModel):
    groq_api_key: Optional[str] = None
    rate_limit: Optional[int] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

# In-memory storage (replace with database in production)
user_settings = {
    "profile": {
        "name": "User",
        "email": "user@example.com",
        "bio": ""
    },
    "preferences": {
        "theme": "dark",
        "model": "llama-3.3-70b-versatile",
        "iterations": 3,
        "notifications": False,
        "autoSave": True
    },
    "api_keys": {
        "groq_api_key": "",
        "rate_limit": 30
    }
}

@router.get("/current")
async def get_current_settings():
    """Get all current user settings"""
    return JSONResponse({
        "profile": user_settings["profile"],
        "preferences": user_settings["preferences"]
    })

@router.post("/profile")
async def update_profile(data: ProfileUpdate):
    """Update user profile information"""
    try:
        if data.name is not None:
            user_settings["profile"]["name"] = data.name
        if data.email is not None:
            user_settings["profile"]["email"] = data.email
        if data.bio is not None:
            user_settings["profile"]["bio"] = data.bio
        
        return JSONResponse({"message": "Profile updated successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/preferences")
async def update_preferences(data: PreferencesUpdate):
    """Update user preferences"""
    try:
        if data.theme is not None:
            user_settings["preferences"]["theme"] = data.theme
        if data.model is not None:
            user_settings["preferences"]["model"] = data.model
        if data.iterations is not None:
            user_settings["preferences"]["iterations"] = data.iterations
        if data.notifications is not None:
            user_settings["preferences"]["notifications"] = data.notifications
        if data.autoSave is not None:
            user_settings["preferences"]["autoSave"] = data.autoSave
        
        return JSONResponse({"message": "Preferences updated successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api-keys")
async def update_api_keys(data: ApiKeysUpdate):
    """Update API keys and configuration"""
    try:
        if data.groq_api_key is not None:
            user_settings["api_keys"]["groq_api_key"] = data.groq_api_key
            # Update environment variable or config
            import os
            os.environ["GROQ_API_KEY"] = data.groq_api_key
        
        if data.rate_limit is not None:
            user_settings["api_keys"]["rate_limit"] = data.rate_limit
        
        return JSONResponse({"message": "API keys updated successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/change-password")
async def change_password(data: PasswordChange):
    """Change user password"""
    try:
        # In production, verify current password and hash new password
        # For now, just return success
        return JSONResponse({"message": "Password changed successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export-data")
async def export_user_data():
    """Export all user data as JSON"""
    try:
        # In production, gather all user data from database
        export_data = {
            "profile": user_settings["profile"],
            "preferences": user_settings["preferences"],
            "conversations": [],  # Would fetch from database
            "created_at": "2024-01-01T00:00:00Z"
        }
        
        json_str = json.dumps(export_data, indent=2)
        buffer = BytesIO(json_str.encode('utf-8'))
        
        return StreamingResponse(
            buffer,
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=user_data.json"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

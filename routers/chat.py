from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import User, Conversation, Message
from auth import get_current_user
from pydantic import BaseModel
from typing import List, Optional
import os
from groq import Groq

router = APIRouter(prefix="/api/chat", tags=["chat"])

# Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
DEFAULT_MODEL = "llama-3.3-70b-versatile"

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

@router.post("")
async def chat_endpoint(
    request: ChatRequest, 
    user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    # 1. Get or Create Conversation
    if request.conversation_id:
        conversation = session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user.id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(title=request.message[:30], user_id=user.id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # 2. Save User Message
    user_msg = Message(conversation_id=conversation.id, role="user", content=request.message)
    session.add(user_msg)
    
    # 3. Build History for Groq
    # Fetch recent messages (limit to 20 for context window efficiency)
    history_msgs = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at.asc())
    ).all()
    
    groq_messages = []
    groq_messages.append({"role": "system", "content": "You are a helpful AI research assistant."})
    
    for m in history_msgs:
        # Map our roles to Groq roles
        role = "assistant" if m.role == "assistant" else "user"
        groq_messages.append({"role": role, "content": m.content})
    
    # 4. Call Groq
    try:
        completion = client.chat.completions.create(
            messages=groq_messages,
            model=DEFAULT_MODEL
        )
        response_text = completion.choices[0].message.content
    except Exception as e:
        print(f"Groq API Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get AI response")
        
    # 5. Save AI Message
    ai_msg = Message(conversation_id=conversation.id, role="assistant", content=response_text)
    session.add(ai_msg)
    session.commit()
    
    return {
        "response": response_text,
        "conversation_id": conversation.id,
        "title": conversation.title
    }

@router.get("/conversations")
async def get_conversations(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    # Sort by descending to show newest on top in sidebar
    convos = session.exec(
        select(Conversation)
        .where(Conversation.user_id == user.id)
        .order_by(Conversation.created_at.desc())
    ).all()
    return convos

@router.get("/{conversation_id}")
async def get_history(conversation_id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    conversation = session.get(Conversation, conversation_id)
    if not conversation or conversation.user_id != user.id:
         raise HTTPException(status_code=404, detail="Conversation not found")
         
    messages = session.exec(select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)).all()
    return messages

@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    conversation = session.get(Conversation, conversation_id)
    if not conversation or conversation.user_id != user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Delete associated messages first (cascading)
    messages = session.exec(select(Message).where(Message.conversation_id == conversation_id)).all()
    for msg in messages:
        session.delete(msg)
    
    session.delete(conversation)
    session.commit()
    return {"detail": "Conversation deleted"}

class RenameRequest(BaseModel):
    title: str

@router.patch("/{conversation_id}")
async def rename_conversation(
    conversation_id: int, 
    request: RenameRequest,
    user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    conversation = session.get(Conversation, conversation_id)
    if not conversation or conversation.user_id != user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conversation.title = request.title
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation

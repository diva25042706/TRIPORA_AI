from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.chat_service import chat_service
from pydantic import BaseModel

class ChatMessageInput(BaseModel):
    message: str

class ChatMessageOutput(BaseModel):
    id: int
    role: str
    content: str
    agent_name: str
    created_at: str

router = APIRouter(prefix="/chat", tags=["AI Travel Chatbot"])

@router.post("/{trip_id}/message")
async def send_message(
    trip_id: str,
    payload: ChatMessageInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Interact with the TRIPORA AI Travel Assistant grounded in the active trip plan."""
    return await chat_service.process_chat_message(
        db=db,
        trip_id=trip_id,
        user_id=current_user.id,
        content=payload.message
    )

@router.get("/{trip_id}/messages")
def get_messages(
    trip_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve saved conversation history for a trip."""
    msgs = chat_service.get_conversation_history(db, trip_id, current_user.id)
    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "agent_name": m.agent_name,
            "created_at": m.created_at.isoformat()
        }
        for m in msgs
    ]

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.chat import ChatConversation, ChatMessage
from pydantic import BaseModel

router = APIRouter()


class MessageSchema(BaseModel):
    id: int
    role: str
    content: str
    has_errors: bool
    corrections: Optional[dict]
    feedback: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationSchema(BaseModel):
    id: int
    language_id: int
    conversation_type: str
    scenario_name: Optional[str]
    ai_character: Optional[str]
    is_active: bool
    started_at: datetime
    messages: List[MessageSchema] = []

    class Config:
        from_attributes = True


class CreateConversationRequest(BaseModel):
    language_id: int
    conversation_type: str = "free"
    scenario_name: Optional[str] = None
    ai_character: Optional[str] = "friendly_tutor"
    difficulty_level: str = "medium"


class SendMessageRequest(BaseModel):
    content: str


@router.post("/conversations", response_model=ConversationSchema, status_code=status.HTTP_201_CREATED)
def create_conversation(
    conversation_data: CreateConversationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Create a new chat conversation"""
    conversation = ChatConversation(
        user_id=current_user.id,
        **conversation_data.dict()
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    # Add initial system message
    from app.services.ai.openai_service import get_initial_chat_prompt

    system_message = ChatMessage(
        conversation_id=conversation.id,
        role="system",
        content=get_initial_chat_prompt(
            conversation_type=conversation_data.conversation_type,
            scenario=conversation_data.scenario_name,
            character=conversation_data.ai_character
        )
    )
    db.add(system_message)
    db.commit()

    return conversation


@router.get("/conversations", response_model=List[ConversationSchema])
def get_conversations(
    language_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get user's chat conversations"""
    query = db.query(ChatConversation).filter(
        ChatConversation.user_id == current_user.id
    )

    if language_id:
        query = query.filter(ChatConversation.language_id == language_id)

    if is_active is not None:
        query = query.filter(ChatConversation.is_active == is_active)

    return query.order_by(ChatConversation.started_at.desc()).offset(skip).limit(limit).all()


@router.get("/conversations/{conversation_id}", response_model=ConversationSchema)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get specific conversation with messages"""
    conversation = db.query(ChatConversation).filter(
        ChatConversation.id == conversation_id,
        ChatConversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    return conversation


@router.post("/conversations/{conversation_id}/messages", response_model=MessageSchema)
async def send_message(
    conversation_id: int,
    message_data: SendMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Send a message in a conversation and get AI response"""
    conversation = db.query(ChatConversation).filter(
        ChatConversation.id == conversation_id,
        ChatConversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    # Save user message
    user_message = ChatMessage(
        conversation_id=conversation_id,
        role="user",
        content=message_data.content
    )
    db.add(user_message)
    db.commit()

    # Get AI response
    from app.services.ai.openai_service import get_chat_response

    ai_response, corrections = await get_chat_response(
        conversation_id=conversation_id,
        user_message=message_data.content,
        db=db
    )

    # Save AI message
    ai_message = ChatMessage(
        conversation_id=conversation_id,
        role="assistant",
        content=ai_response,
        corrections=corrections
    )
    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)

    return ai_message


@router.delete("/conversations/{conversation_id}")
def end_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """End a conversation"""
    conversation = db.query(ChatConversation).filter(
        ChatConversation.id == conversation_id,
        ChatConversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    conversation.is_active = False
    conversation.ended_at = datetime.utcnow()
    db.commit()

    return {"message": "Conversation ended"}

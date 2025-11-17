from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class ChatConversation(Base):
    __tablename__ = "chat_conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)

    # Conversation type
    conversation_type = Column(String(50), default="free")  # free, scenario
    scenario_name = Column(String(200))  # restaurant, airport, job_interview, etc.

    # AI personality
    ai_character = Column(String(100))  # friendly_tutor, strict_teacher, native_speaker, etc.
    ai_personality_prompt = Column(Text)

    # Settings
    difficulty_level = Column(String(20))  # easy, medium, hard
    correction_mode = Column(String(50), default="immediate")  # immediate, end, none

    # Status
    is_active = Column(Boolean, default=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True))

    # Relationships
    user = relationship("User", back_populates="chat_conversations")
    language = relationship("Language")
    messages = relationship("ChatMessage", back_populates="conversation", order_by="ChatMessage.created_at")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("chat_conversations.id"), nullable=False)

    # Message content
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)

    # Corrections and feedback (if applicable)
    has_errors = Column(Boolean, default=False)
    corrections = Column(JSON)  # List of corrections
    feedback = Column(Text)

    # Metadata
    tokens_used = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    conversation = relationship("ChatConversation", back_populates="messages")

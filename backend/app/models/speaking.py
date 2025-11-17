from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class SpeakingSession(Base):
    __tablename__ = "speaking_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)

    # Session type
    session_type = Column(String(50))  # conversation, pronunciation, scenario
    scenario_name = Column(String(200))
    topic = Column(String(200))

    # Difficulty
    difficulty_level = Column(String(20))

    # Session duration
    duration_seconds = Column(Integer)

    # Overall scores
    overall_score = Column(Float)
    pronunciation_score = Column(Float)
    fluency_score = Column(Float)
    accuracy_score = Column(Float)

    # XP earned
    xp_earned = Column(Integer)

    # Status
    is_completed = Column(Boolean, default=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))

    # Relationships
    user = relationship("User", back_populates="speaking_sessions")
    language = relationship("Language")
    recordings = relationship("SpeakingRecording", back_populates="session")
    evaluation = relationship("SpeakingEvaluation", back_populates="session", uselist=False)


class SpeakingRecording(Base):
    __tablename__ = "speaking_recordings"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("speaking_sessions.id"), nullable=False)

    # Recording details
    audio_url = Column(String(500), nullable=False)
    duration_seconds = Column(Integer)

    # Transcription
    transcription = Column(Text)
    expected_text = Column(Text)  # For pronunciation practice

    # Scores
    pronunciation_score = Column(Float)
    accuracy_score = Column(Float)
    fluency_score = Column(Float)

    # Word-level analysis
    word_scores = Column(JSON)  # Individual word pronunciation scores

    # Order in session
    order = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    session = relationship("SpeakingSession", back_populates="recordings")


class SpeakingEvaluation(Base):
    __tablename__ = "speaking_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("speaking_sessions.id"), unique=True, nullable=False)

    # Detailed feedback
    strengths = Column(JSON)  # List of strengths
    weaknesses = Column(JSON)  # List of weaknesses
    suggestions = Column(JSON)  # Improvement suggestions

    # Common mistakes
    pronunciation_issues = Column(JSON)
    grammar_issues = Column(JSON)
    vocabulary_suggestions = Column(JSON)

    # AI-generated feedback
    ai_feedback = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    session = relationship("SpeakingSession", back_populates="evaluation")

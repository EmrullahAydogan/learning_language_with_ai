from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class WritingSubmission(Base):
    __tablename__ = "writing_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)

    # Prompt/topic
    prompt = Column(Text)
    topic = Column(String(200))
    writing_type = Column(String(50))  # essay, email, creative, diary, etc.

    # Content
    title = Column(String(300))
    content = Column(Text, nullable=False)
    word_count = Column(Integer)

    # Time tracking
    time_spent_seconds = Column(Integer)

    # XP earned
    xp_earned = Column(Integer)

    # Dates
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="writing_submissions")
    language = relationship("Language")
    evaluation = relationship("WritingEvaluation", back_populates="submission", uselist=False)


class WritingEvaluation(Base):
    __tablename__ = "writing_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("writing_submissions.id"), unique=True, nullable=False)

    # Overall scores
    overall_score = Column(Float)
    grammar_score = Column(Float)
    vocabulary_score = Column(Float)
    coherence_score = Column(Float)
    style_score = Column(Float)

    # Detailed feedback
    grammar_errors = Column(JSON)  # List of grammar errors with corrections
    spelling_errors = Column(JSON)  # List of spelling errors
    vocabulary_suggestions = Column(JSON)  # Vocabulary improvement suggestions
    style_suggestions = Column(JSON)  # Style improvement suggestions

    # Strengths and weaknesses
    strengths = Column(JSON)
    weaknesses = Column(JSON)

    # AI-generated feedback
    ai_feedback = Column(Text)
    corrected_version = Column(Text)  # AI-corrected version

    # Statistics
    unique_words_count = Column(Integer)
    average_sentence_length = Column(Float)
    readability_score = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    submission = relationship("WritingSubmission", back_populates="evaluation")

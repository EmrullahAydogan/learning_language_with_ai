"""
Assessment models for language proficiency testing
"""

from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class LevelAssessment(Base):
    """
    User's language level assessment
    """
    __tablename__ = "level_assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    determined_level_id = Column(Integer, ForeignKey("proficiency_levels.id"), nullable=True)

    score_percentage = Column(Float, nullable=True)
    correct_answers = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)

    is_completed = Column(Boolean, default=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="assessments")
    language = relationship("Language")
    determined_level = relationship("ProficiencyLevel")
    answers = relationship("AssessmentAnswer", back_populates="assessment", cascade="all, delete-orphan")


class AssessmentQuestion(Base):
    """
    Questions for language level assessment
    Covers multiple proficiency levels to determine user's level
    """
    __tablename__ = "assessment_questions"

    id = Column(Integer, primary_key=True, index=True)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    proficiency_level_id = Column(Integer, ForeignKey("proficiency_levels.id"), nullable=False)

    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)  # multiple_choice, fill_blank, etc.

    # For multiple choice
    options = Column(JSON, nullable=True)  # List of options
    correct_answer = Column(String(500), nullable=False)

    explanation = Column(Text, nullable=True)
    order = Column(Integer, default=0)
    difficulty_weight = Column(Integer, default=1)  # For scoring

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    language = relationship("Language")
    proficiency_level = relationship("ProficiencyLevel")
    answers = relationship("AssessmentAnswer", back_populates="question")


class AssessmentAnswer(Base):
    """
    User's answers to assessment questions
    """
    __tablename__ = "assessment_answers"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("level_assessments.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("assessment_questions.id"), nullable=False)

    user_answer = Column(String(500), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    time_spent_seconds = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    assessment = relationship("LevelAssessment", back_populates="answers")
    question = relationship("AssessmentQuestion", back_populates="answers")

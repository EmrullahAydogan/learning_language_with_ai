from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, DateTime, JSON, Boolean, Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class ExerciseType(Base):
    __tablename__ = "exercise_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    icon = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    exercise_type_id = Column(Integer, ForeignKey("exercise_types.id"), nullable=False)
    proficiency_level_id = Column(Integer, ForeignKey("proficiency_levels.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))

    title = Column(String(200), nullable=False)
    description = Column(Text)
    instructions = Column(Text)

    # Difficulty and points
    difficulty = Column(String(20))  # easy, medium, hard
    xp_reward = Column(Integer, default=10)
    estimated_time_minutes = Column(Integer)

    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    language = relationship("Language")
    exercise_type = relationship("ExerciseType")
    proficiency_level = relationship("ProficiencyLevel")
    topic = relationship("Topic")
    questions = relationship("ExerciseQuestion", back_populates="exercise")


class ExerciseQuestion(Base):
    __tablename__ = "exercise_questions"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)

    question_text = Column(Text, nullable=False)
    question_audio_url = Column(String(500))
    question_image_url = Column(String(500))

    # Answer data (flexible JSON structure for different question types)
    # MCQ: {"options": ["A", "B", "C"], "correct": 0}
    # Fill blank: {"correct": ["answer1", "answer2"]}
    # Matching: {"pairs": [[0,2], [1,3], ...]}
    answer_data = Column(JSON, nullable=False)

    # Explanation
    explanation = Column(Text)
    explanation_audio_url = Column(String(500))

    # Order in exercise
    order = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    exercise = relationship("Exercise", back_populates="questions")


class UserExerciseHistory(Base):
    __tablename__ = "user_exercise_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)

    # Results
    score = Column(Float)  # Percentage
    total_questions = Column(Integer)
    correct_answers = Column(Integer)
    time_taken_seconds = Column(Integer)

    # XP earned
    xp_earned = Column(Integer)

    # Answers given
    answers = Column(JSON)  # Store user's answers

    # Completion
    completed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="exercise_history")
    exercise = relationship("Exercise")

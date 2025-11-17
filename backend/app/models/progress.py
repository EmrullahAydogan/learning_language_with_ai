from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)

    # Vocabulary stats
    total_words_learned = Column(Integer, default=0)
    words_mastered = Column(Integer, default=0)
    words_learning = Column(Integer, default=0)

    # Exercise stats
    total_exercises_completed = Column(Integer, default=0)
    total_exercises_correct = Column(Integer, default=0)
    average_exercise_score = Column(Float, default=0)

    # Speaking stats
    total_speaking_sessions = Column(Integer, default=0)
    total_speaking_minutes = Column(Integer, default=0)
    average_pronunciation_score = Column(Float, default=0)

    # Reading stats
    total_articles_read = Column(Integer, default=0)
    total_reading_minutes = Column(Integer, default=0)

    # Writing stats
    total_writings_submitted = Column(Integer, default=0)
    average_writing_score = Column(Float, default=0)

    # Chat stats
    total_chat_messages = Column(Integer, default=0)

    # Time stats
    total_study_time_minutes = Column(Integer, default=0)

    # Last activity
    last_activity_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="progress")
    language = relationship("Language")


class DailyActivity(Base):
    __tablename__ = "daily_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"))
    date = Column(DateTime(timezone=True), nullable=False, index=True)

    # Activity counts
    words_reviewed = Column(Integer, default=0)
    words_learned = Column(Integer, default=0)
    exercises_completed = Column(Integer, default=0)
    speaking_minutes = Column(Integer, default=0)
    reading_minutes = Column(Integer, default=0)
    writing_minutes = Column(Integer, default=0)
    chat_messages = Column(Integer, default=0)

    # Total study time
    study_time_minutes = Column(Integer, default=0)

    # XP earned today
    xp_earned = Column(Integer, default=0)

    # Goal completion
    daily_goal_met = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="daily_activities")
    language = relationship("Language")


class Streak(Base):
    __tablename__ = "streaks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Current streak
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)

    # Dates
    last_activity_date = Column(DateTime(timezone=True))
    streak_started_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="streaks")


class UserXP(Base):
    __tablename__ = "user_xp"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # Total XP
    total_xp = Column(Integer, default=0)

    # XP by category
    vocabulary_xp = Column(Integer, default=0)
    exercise_xp = Column(Integer, default=0)
    speaking_xp = Column(Integer, default=0)
    reading_xp = Column(Integer, default=0)
    writing_xp = Column(Integer, default=0)
    chat_xp = Column(Integer, default=0)

    # Daily/Weekly XP
    today_xp = Column(Integer, default=0)
    week_xp = Column(Integer, default=0)

    # Last XP reset dates
    last_daily_reset = Column(DateTime(timezone=True))
    last_weekly_reset = Column(DateTime(timezone=True))

    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="xp")


class UserLevel(Base):
    __tablename__ = "user_levels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # Current level (1-100)
    current_level = Column(Integer, default=1)

    # XP for current level
    current_level_xp = Column(Integer, default=0)
    xp_to_next_level = Column(Integer, default=100)

    # Level history
    total_levels_gained = Column(Integer, default=0)

    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="level")

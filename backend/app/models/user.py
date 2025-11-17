from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    languages = relationship("UserLanguage", back_populates="user")
    preferences = relationship("UserPreference", back_populates="user", uselist=False)
    progress = relationship("UserProgress", back_populates="user")
    vocabulary_progress = relationship("UserVocabulary", back_populates="user")
    exercise_history = relationship("UserExerciseHistory", back_populates="user")
    chat_conversations = relationship("ChatConversation", back_populates="user")
    speaking_sessions = relationship("SpeakingSession", back_populates="user")
    reading_history = relationship("UserReadingHistory", back_populates="user")
    writing_submissions = relationship("WritingSubmission", back_populates="user")
    daily_activities = relationship("DailyActivity", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")
    xp = relationship("UserXP", back_populates="user", uselist=False)
    level = relationship("UserLevel", back_populates="user", uselist=False)
    streaks = relationship("Streak", back_populates="user")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    date_of_birth = Column(DateTime)
    avatar_url = Column(String(500))
    bio = Column(Text)
    native_language_id = Column(Integer, ForeignKey("languages.id"))
    timezone = Column(String(50), default="UTC")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")
    native_language = relationship("Language")


class UserLanguage(Base):
    __tablename__ = "user_languages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    language_id = Column(Integer, ForeignKey("languages.id"))
    proficiency_level_id = Column(Integer, ForeignKey("proficiency_levels.id"))
    is_primary = Column(Boolean, default=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    target_level_id = Column(Integer, ForeignKey("proficiency_levels.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="languages")
    language = relationship("Language")
    proficiency_level = relationship("ProficiencyLevel", foreign_keys=[proficiency_level_id])
    target_level = relationship("ProficiencyLevel", foreign_keys=[target_level_id])


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    daily_goal_minutes = Column(Integer, default=15)
    daily_goal_xp = Column(Integer, default=50)
    new_words_per_day = Column(Integer, default=10)
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    reminder_time = Column(String(10))  # HH:MM format
    difficulty_preference = Column(String(20), default="adaptive")  # easy, medium, hard, adaptive
    audio_speed = Column(Integer, default=100)  # percentage
    show_translation = Column(Boolean, default=True)
    theme = Column(String(20), default="light")  # light, dark, auto
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="preferences")

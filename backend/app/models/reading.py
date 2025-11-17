from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class ReadingMaterial(Base):
    __tablename__ = "reading_materials"

    id = Column(Integer, primary_key=True, index=True)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    proficiency_level_id = Column(Integer, ForeignKey("proficiency_levels.id"))

    # Content
    title = Column(String(300), nullable=False)
    subtitle = Column(String(500))
    content = Column(Text, nullable=False)
    content_type = Column(String(50))  # article, story, news, dialogue

    # Author and source
    author = Column(String(200))
    source = Column(String(200))
    source_url = Column(String(500))

    # Metadata
    word_count = Column(Integer)
    estimated_reading_time_minutes = Column(Integer)
    difficulty = Column(String(20))

    # Topics/tags
    topics = Column(JSON)  # List of topics
    tags = Column(JSON)  # List of tags

    # Comprehension questions
    has_questions = Column(Boolean, default=False)
    questions = Column(JSON)  # List of comprehension questions

    # Media
    image_url = Column(String(500))
    audio_url = Column(String(500))

    # Status
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    language = relationship("Language")
    proficiency_level = relationship("ProficiencyLevel")


class UserReadingHistory(Base):
    __tablename__ = "user_reading_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reading_material_id = Column(Integer, ForeignKey("reading_materials.id"), nullable=False)

    # Reading progress
    is_completed = Column(Boolean, default=False)
    completion_percentage = Column(Integer, default=0)
    time_spent_seconds = Column(Integer)

    # Comprehension quiz results
    quiz_score = Column(Integer)  # Percentage
    quiz_answers = Column(JSON)

    # Words looked up
    words_looked_up = Column(JSON)  # List of words user clicked for definition

    # XP earned
    xp_earned = Column(Integer)

    # Bookmarking
    is_bookmarked = Column(Boolean, default=False)

    # Dates
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    last_read_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="reading_history")
    reading_material = relationship("ReadingMaterial")

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    icon = Column(String(50))
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    lessons = relationship("Lesson", back_populates="topic")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    proficiency_level_id = Column(Integer, ForeignKey("proficiency_levels.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))

    title = Column(String(200), nullable=False)
    description = Column(Text)
    content = Column(Text)  # Lesson content in markdown/HTML

    # Grammar focus
    grammar_points = Column(Text)

    # Order
    order = Column(Integer, default=0)

    # Metadata
    estimated_time_minutes = Column(Integer)
    is_premium = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    language = relationship("Language")
    proficiency_level = relationship("ProficiencyLevel")
    topic = relationship("Topic", back_populates="lessons")

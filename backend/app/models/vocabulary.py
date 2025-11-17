from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, DateTime, JSON, Float, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class VocabularyCategory(Base):
    __tablename__ = "vocabulary_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    icon = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Vocabulary(Base):
    __tablename__ = "vocabulary"

    id = Column(Integer, primary_key=True, index=True)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    word = Column(String(200), nullable=False, index=True)
    translation = Column(String(200))
    pronunciation = Column(String(200))
    phonetic = Column(String(200))
    part_of_speech = Column(String(50))  # noun, verb, adjective, etc.
    difficulty_level_id = Column(Integer, ForeignKey("proficiency_levels.id"))
    category_id = Column(Integer, ForeignKey("vocabulary_categories.id"))

    # Definitions and examples
    definition = Column(Text)
    example_sentence = Column(Text)
    example_translation = Column(Text)

    # Additional info
    synonyms = Column(JSON)  # List of synonyms
    antonyms = Column(JSON)  # List of antonyms
    related_words = Column(JSON)  # Related words

    # Media
    image_url = Column(String(500))
    audio_url = Column(String(500))

    # Metadata
    frequency = Column(Integer, default=0)  # Word frequency ranking
    is_common = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    language = relationship("Language")
    difficulty_level = relationship("ProficiencyLevel")
    category = relationship("VocabularyCategory")


class UserVocabulary(Base):
    """Tracks user's vocabulary learning progress (flashcard system)"""
    __tablename__ = "user_vocabulary"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vocabulary_id = Column(Integer, ForeignKey("vocabulary.id"), nullable=False)

    # Spaced Repetition Algorithm (SM-2) fields
    ease_factor = Column(Float, default=2.5)  # Ease factor (2.5 is default)
    interval = Column(Integer, default=0)  # Days until next review
    repetitions = Column(Integer, default=0)  # Number of successful repetitions
    next_review_date = Column(DateTime(timezone=True))

    # Learning status
    status = Column(String(20), default="new")  # new, learning, review, mastered
    times_reviewed = Column(Integer, default=0)
    times_correct = Column(Integer, default=0)
    times_incorrect = Column(Integer, default=0)

    # Dates
    first_seen_at = Column(DateTime(timezone=True), server_default=func.now())
    last_reviewed_at = Column(DateTime(timezone=True))
    mastered_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="vocabulary_progress")
    vocabulary = relationship("Vocabulary")
    reviews = relationship("FlashcardReview", back_populates="user_vocabulary")


class FlashcardReview(Base):
    """Individual review history for flashcards"""
    __tablename__ = "flashcard_reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_vocabulary_id = Column(Integer, ForeignKey("user_vocabulary.id"), nullable=False)

    # Review details
    quality = Column(Integer)  # 0-5 scale (SM-2 algorithm)
    time_taken_seconds = Column(Integer)
    was_correct = Column(Boolean)

    # Context
    review_type = Column(String(50))  # recognition, recall, production
    reviewed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user_vocabulary = relationship("UserVocabulary", back_populates="reviews")

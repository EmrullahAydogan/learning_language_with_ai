from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    icon = Column(String(100))
    category = Column(String(50))  # vocabulary, speaking, writing, streak, etc.
    rarity = Column(String(20))  # common, rare, epic, legendary

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)

    # Achievement criteria
    achievement_type = Column(String(50), nullable=False)  # word_count, streak, exercise_count, etc.
    target_value = Column(Integer, nullable=False)  # Target to achieve
    xp_reward = Column(Integer, default=0)

    # Metadata
    is_active = Column(Boolean, default=True)
    is_repeatable = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    badge = relationship("Badge")


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)

    # Progress
    current_progress = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)

    # Dates
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))

    # Times completed (for repeatable achievements)
    times_completed = Column(Integer, default=0)

    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement")


class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    challenge_type = Column(String(50))  # daily, weekly, special

    # Challenge criteria
    criteria = Column(JSON)  # Flexible structure for different challenge types

    # Rewards
    xp_reward = Column(Integer, default=0)
    badge_reward_id = Column(Integer, ForeignKey("badges.id"))

    # Timing
    starts_at = Column(DateTime(timezone=True))
    ends_at = Column(DateTime(timezone=True))

    # Status
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    badge_reward = relationship("Badge")


class UserChallenge(Base):
    __tablename__ = "user_challenges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)

    # Progress
    progress_data = Column(JSON)  # Flexible structure for tracking progress
    is_completed = Column(Boolean, default=False)

    # Dates
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))

    # Relationships
    user = relationship("User")
    challenge = relationship("Challenge")

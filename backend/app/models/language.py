from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.sql import func
from app.db.session import Base


class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, index=True, nullable=False)  # en, es, fr, etc.
    name = Column(String(100), nullable=False)  # English, Spanish, French
    native_name = Column(String(100), nullable=False)  # English, Español, Français
    flag = Column(String(10))  # emoji flag
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ProficiencyLevel(Base):
    __tablename__ = "proficiency_levels"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, index=True, nullable=False)  # A1, A2, B1, B2, C1, C2
    name = Column(String(50), nullable=False)  # Beginner, Elementary, etc.
    description = Column(Text)
    order = Column(Integer)  # For sorting
    created_at = Column(DateTime(timezone=True), server_default=func.now())

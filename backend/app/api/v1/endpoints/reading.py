from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.reading import ReadingMaterial, UserReadingHistory
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class ReadingMaterialSchema(BaseModel):
    id: int
    title: str
    subtitle: Optional[str]
    content: str
    content_type: Optional[str]
    word_count: Optional[int]
    estimated_reading_time_minutes: Optional[int]
    difficulty: Optional[str]
    image_url: Optional[str]

    class Config:
        from_attributes = True


class StartReadingRequest(BaseModel):
    reading_material_id: int


class CompleteReadingRequest(BaseModel):
    time_spent_seconds: int
    quiz_answers: Optional[dict] = None
    words_looked_up: Optional[list] = None


@router.get("/materials", response_model=List[ReadingMaterialSchema])
def get_reading_materials(
    language_id: int = Query(...),
    level_id: Optional[int] = None,
    content_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get available reading materials"""
    query = db.query(ReadingMaterial).filter(
        ReadingMaterial.language_id == language_id,
        ReadingMaterial.is_active == True
    )

    if level_id:
        query = query.filter(ReadingMaterial.proficiency_level_id == level_id)

    if content_type:
        query = query.filter(ReadingMaterial.content_type == content_type)

    return query.offset(skip).limit(limit).all()


@router.post("/start")
def start_reading(
    reading_data: StartReadingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Start reading a material"""
    # Check if already started
    existing = db.query(UserReadingHistory).filter(
        UserReadingHistory.user_id == current_user.id,
        UserReadingHistory.reading_material_id == reading_data.reading_material_id,
        UserReadingHistory.is_completed == False
    ).first()

    if existing:
        return existing

    history = UserReadingHistory(
        user_id=current_user.id,
        reading_material_id=reading_data.reading_material_id
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


@router.post("/complete/{history_id}")
def complete_reading(
    history_id: int,
    completion_data: CompleteReadingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Complete a reading session"""
    history = db.query(UserReadingHistory).filter(
        UserReadingHistory.id == history_id,
        UserReadingHistory.user_id == current_user.id
    ).first()

    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading history not found"
        )

    history.is_completed = True
    history.completion_percentage = 100
    history.time_spent_seconds = completion_data.time_spent_seconds
    history.completed_at = datetime.utcnow()

    if completion_data.quiz_answers:
        history.quiz_answers = completion_data.quiz_answers
        # Calculate quiz score here if needed

    if completion_data.words_looked_up:
        history.words_looked_up = completion_data.words_looked_up

    db.commit()
    return {"message": "Reading completed successfully"}


@router.get("/history", response_model=List[UserReadingHistory])
def get_reading_history(
    language_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get user's reading history"""
    query = db.query(UserReadingHistory).filter(
        UserReadingHistory.user_id == current_user.id
    )

    if language_id:
        query = query.join(ReadingMaterial).filter(
            ReadingMaterial.language_id == language_id
        )

    return query.order_by(UserReadingHistory.started_at.desc()).offset(skip).limit(limit).all()

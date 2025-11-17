from typing import Any, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.progress import UserProgress, DailyActivity, Streak, UserXP, UserLevel
from pydantic import BaseModel

router = APIRouter()


class UserProgressSchema(BaseModel):
    total_words_learned: int
    words_mastered: int
    total_exercises_completed: int
    average_exercise_score: float
    total_speaking_sessions: int
    total_study_time_minutes: int

    class Config:
        from_attributes = True


class DailyActivitySchema(BaseModel):
    date: datetime
    words_reviewed: int
    exercises_completed: int
    study_time_minutes: int
    xp_earned: int
    daily_goal_met: bool

    class Config:
        from_attributes = True


class StreakSchema(BaseModel):
    current_streak: int
    longest_streak: int
    last_activity_date: Optional[datetime]

    class Config:
        from_attributes = True


class UserXPSchema(BaseModel):
    total_xp: int
    vocabulary_xp: int
    exercise_xp: int
    speaking_xp: int
    reading_xp: int
    writing_xp: int
    today_xp: int
    week_xp: int

    class Config:
        from_attributes = True


class UserLevelSchema(BaseModel):
    current_level: int
    current_level_xp: int
    xp_to_next_level: int
    total_levels_gained: int

    class Config:
        from_attributes = True


@router.get("/overview")
def get_progress_overview(
    language_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get overall progress overview"""
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.language_id == language_id
    ).first()

    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            language_id=language_id
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)

    return progress


@router.get("/daily-activity")
def get_daily_activity(
    language_id: Optional[int] = None,
    days: int = Query(7, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get daily activity for the past N days"""
    start_date = datetime.utcnow() - timedelta(days=days)

    query = db.query(DailyActivity).filter(
        DailyActivity.user_id == current_user.id,
        DailyActivity.date >= start_date
    )

    if language_id:
        query = query.filter(DailyActivity.language_id == language_id)

    activities = query.order_by(DailyActivity.date.desc()).all()
    return activities


@router.get("/streak", response_model=StreakSchema)
def get_streak(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get user's learning streak"""
    streak = db.query(Streak).filter(Streak.user_id == current_user.id).first()

    if not streak:
        streak = Streak(user_id=current_user.id)
        db.add(streak)
        db.commit()
        db.refresh(streak)

    return streak


@router.get("/xp", response_model=UserXPSchema)
def get_user_xp(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get user's XP information"""
    xp = db.query(UserXP).filter(UserXP.user_id == current_user.id).first()

    if not xp:
        xp = UserXP(user_id=current_user.id)
        db.add(xp)
        db.commit()
        db.refresh(xp)

    return xp


@router.get("/level", response_model=UserLevelSchema)
def get_user_level(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get user's level information"""
    level = db.query(UserLevel).filter(UserLevel.user_id == current_user.id).first()

    if not level:
        level = UserLevel(user_id=current_user.id)
        db.add(level)
        db.commit()
        db.refresh(level)

    return level

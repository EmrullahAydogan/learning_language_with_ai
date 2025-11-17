from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.gamification import Achievement, Badge, UserAchievement, Challenge, UserChallenge
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class BadgeSchema(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    category: str
    rarity: str

    class Config:
        from_attributes = True


class AchievementSchema(BaseModel):
    id: int
    achievement_type: str
    target_value: int
    xp_reward: int
    badge: BadgeSchema

    class Config:
        from_attributes = True


class UserAchievementSchema(BaseModel):
    id: int
    achievement_id: int
    current_progress: int
    is_completed: bool
    completed_at: Optional[datetime]
    achievement: AchievementSchema

    class Config:
        from_attributes = True


@router.get("/achievements", response_model=List[AchievementSchema])
def get_all_achievements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get all available achievements"""
    return db.query(Achievement).filter(Achievement.is_active == True).all()


@router.get("/achievements/user", response_model=List[UserAchievementSchema])
def get_user_achievements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get user's achievements"""
    return db.query(UserAchievement).filter(
        UserAchievement.user_id == current_user.id
    ).all()


@router.get("/badges", response_model=List[BadgeSchema])
def get_all_badges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get all available badges"""
    return db.query(Badge).all()


@router.get("/challenges/active")
def get_active_challenges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get active challenges"""
    now = datetime.utcnow()
    return db.query(Challenge).filter(
        Challenge.is_active == True,
        Challenge.starts_at <= now,
        Challenge.ends_at >= now
    ).all()

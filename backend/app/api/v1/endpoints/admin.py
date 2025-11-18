"""
Admin panel API endpoints for platform management
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.vocabulary import Vocabulary, VocabularyCategory
from app.models.exercise import Exercise
from app.models.reading import ReadingMaterial
from app.models.gamification import Achievement, Badge
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


def require_admin(current_user: User = Depends(get_current_user)):
    """Dependency to require admin privileges"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user


# ========== Platform Statistics ==========

@router.get("/stats/overview")
def get_platform_overview(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Get overall platform statistics"""

    # Total users
    total_users = db.query(func.count(User.id)).scalar()

    # Active users (logged in last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    active_users = db.query(func.count(User.id)).filter(
        User.updated_at >= thirty_days_ago
    ).scalar()

    # Total content
    total_vocabulary = db.query(func.count(Vocabulary.id)).scalar()
    total_exercises = db.query(func.count(Exercise.id)).scalar()
    total_reading_materials = db.query(func.count(ReadingMaterial.id)).scalar()
    total_achievements = db.query(func.count(Achievement.id)).scalar()

    # Recent registrations (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    new_users_week = db.query(func.count(User.id)).filter(
        User.created_at >= seven_days_ago
    ).scalar()

    return {
        "users": {
            "total": total_users,
            "active_last_30_days": active_users,
            "new_last_7_days": new_users_week
        },
        "content": {
            "vocabulary_words": total_vocabulary,
            "exercises": total_exercises,
            "reading_materials": total_reading_materials,
            "achievements": total_achievements
        },
        "timestamp": datetime.utcnow().isoformat()
    }


# ========== User Management ==========

@router.get("/users")
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_verified: Optional[bool] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """List all users with filters"""

    query = db.query(User)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (User.username.ilike(search_filter)) |
            (User.email.ilike(search_filter))
        )

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    if is_verified is not None:
        query = query.filter(User.is_verified == is_verified)

    total = query.count()
    users = query.order_by(desc(User.created_at)).offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "is_verified": user.is_verified,
                "is_superuser": user.is_superuser,
                "created_at": user.created_at.isoformat() if user.created_at else None,
            }
            for user in users
        ]
    }


@router.patch("/users/{user_id}/status")
def update_user_status(
    user_id: int,
    is_active: Optional[bool] = None,
    is_verified: Optional[bool] = None,
    is_superuser: Optional[bool] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Update user status (activate/deactivate, verify, admin)"""

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if is_active is not None:
        user.is_active = is_active

    if is_verified is not None:
        user.is_verified = is_verified

    if is_superuser is not None:
        # Prevent removing last admin
        if not is_superuser and user.is_superuser:
            admin_count = db.query(func.count(User.id)).filter(
                User.is_superuser == True
            ).scalar()
            if admin_count <= 1:
                raise HTTPException(
                    status_code=400,
                    detail="Cannot remove last admin user"
                )
        user.is_superuser = is_superuser

    db.commit()
    db.refresh(user)

    return {
        "message": "User status updated",
        "user": {
            "id": user.id,
            "username": user.username,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "is_superuser": user.is_superuser
        }
    }


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Delete a user (soft delete by deactivating)"""

    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Soft delete by deactivating
    user.is_active = False
    db.commit()

    return {"message": f"User {user.username} has been deactivated"}


# ========== Content Management ==========

class VocabularyCreate(BaseModel):
    language_id: int
    difficulty_level_id: int
    category_id: Optional[int] = None
    word: str
    translation: str
    pronunciation: Optional[str] = None
    part_of_speech: Optional[str] = None
    definition: Optional[str] = None
    example_sentence: Optional[str] = None


@router.post("/vocabulary")
def create_vocabulary(
    vocab: VocabularyCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Create new vocabulary word"""

    new_vocab = Vocabulary(**vocab.dict())
    db.add(new_vocab)
    db.commit()
    db.refresh(new_vocab)

    return {
        "message": "Vocabulary created",
        "vocabulary": {
            "id": new_vocab.id,
            "word": new_vocab.word,
            "translation": new_vocab.translation
        }
    }


@router.delete("/vocabulary/{vocab_id}")
def delete_vocabulary(
    vocab_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Delete vocabulary word"""

    vocab = db.query(Vocabulary).filter(Vocabulary.id == vocab_id).first()
    if not vocab:
        raise HTTPException(status_code=404, detail="Vocabulary not found")

    db.delete(vocab)
    db.commit()

    return {"message": "Vocabulary deleted"}


@router.get("/content/stats")
def get_content_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Get detailed content statistics"""

    from sqlalchemy import func
    from app.models.language import Language

    # Vocabulary by language
    vocab_by_language = db.query(
        Language.name,
        func.count(Vocabulary.id).label("count")
    ).join(Vocabulary).group_by(Language.id, Language.name).all()

    # Exercises by language
    exercises_by_language = db.query(
        Language.name,
        func.count(Exercise.id).label("count")
    ).join(Exercise).group_by(Language.id, Language.name).all()

    return {
        "vocabulary_by_language": [
            {"language": lang, "count": count}
            for lang, count in vocab_by_language
        ],
        "exercises_by_language": [
            {"language": lang, "count": count}
            for lang, count in exercises_by_language
        ],
        "total_categories": db.query(func.count(VocabularyCategory.id)).scalar(),
        "total_achievements": db.query(func.count(Achievement.id)).scalar(),
        "total_badges": db.query(func.count(Badge.id)).scalar()
    }


# ========== System Management ==========

@router.post("/cache/clear")
def clear_system_cache(
    admin: User = Depends(require_admin)
):
    """Clear system caches"""

    try:
        # Clear TTS cache
        from app.services.tts import tts_service
        tts_removed = tts_service.clear_cache(max_age_days=7)

        return {
            "message": "Cache cleared successfully",
            "tts_files_removed": tts_removed
        }
    except Exception as e:
        logger.error(f"Cache clearing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")


@router.get("/logs/recent")
def get_recent_logs(
    lines: int = Query(100, ge=1, le=1000),
    admin: User = Depends(require_admin)
):
    """Get recent log entries (if log file exists)"""

    try:
        log_file = "logs/app.log"
        from pathlib import Path

        log_path = Path(log_file)
        if not log_path.exists():
            return {"message": "Log file not found", "logs": []}

        with open(log_path, "r") as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:]

        return {
            "total_lines": len(all_lines),
            "returned_lines": len(recent_lines),
            "logs": recent_lines
        }

    except Exception as e:
        logger.error(f"Failed to read logs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to read logs: {str(e)}")

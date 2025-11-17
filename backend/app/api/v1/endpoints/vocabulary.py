from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.vocabulary import Vocabulary, UserVocabulary, FlashcardReview
from pydantic import BaseModel

router = APIRouter()


class VocabularySchema(BaseModel):
    id: int
    word: str
    translation: Optional[str]
    pronunciation: Optional[str]
    part_of_speech: Optional[str]
    definition: Optional[str]
    example_sentence: Optional[str]
    image_url: Optional[str]
    audio_url: Optional[str]

    class Config:
        from_attributes = True


class UserVocabularySchema(BaseModel):
    id: int
    vocabulary_id: int
    status: str
    ease_factor: float
    interval: int
    next_review_date: Optional[datetime]
    times_reviewed: int
    times_correct: int
    times_incorrect: int
    vocabulary: VocabularySchema

    class Config:
        from_attributes = True


class FlashcardReviewRequest(BaseModel):
    vocabulary_id: int
    quality: int  # 0-5
    time_taken_seconds: int


@router.get("/due", response_model=List[UserVocabularySchema])
def get_due_flashcards(
    language_id: int = Query(...),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get flashcards due for review"""
    now = datetime.utcnow()

    # Get user's vocabulary that's due for review
    user_vocab = db.query(UserVocabulary).join(Vocabulary).filter(
        UserVocabulary.user_id == current_user.id,
        Vocabulary.language_id == language_id,
        UserVocabulary.next_review_date <= now
    ).limit(limit).all()

    return user_vocab


@router.get("/new", response_model=List[VocabularySchema])
def get_new_vocabulary(
    language_id: int = Query(...),
    level_id: Optional[int] = None,
    category_id: Optional[int] = None,
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get new vocabulary words to learn"""
    query = db.query(Vocabulary).filter(
        Vocabulary.language_id == language_id
    )

    # Exclude already learned words
    learned_ids = db.query(UserVocabulary.vocabulary_id).filter(
        UserVocabulary.user_id == current_user.id
    ).all()
    if learned_ids:
        query = query.filter(~Vocabulary.id.in_([id[0] for id in learned_ids]))

    if level_id:
        query = query.filter(Vocabulary.difficulty_level_id == level_id)

    if category_id:
        query = query.filter(Vocabulary.category_id == category_id)

    return query.limit(limit).all()


@router.post("/review", status_code=status.HTTP_201_CREATED)
def review_flashcard(
    review_data: FlashcardReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Submit a flashcard review"""
    from app.services.flashcard.spaced_repetition import update_flashcard_review

    # Get or create user vocabulary
    user_vocab = db.query(UserVocabulary).filter(
        UserVocabulary.user_id == current_user.id,
        UserVocabulary.vocabulary_id == review_data.vocabulary_id
    ).first()

    if not user_vocab:
        user_vocab = UserVocabulary(
            user_id=current_user.id,
            vocabulary_id=review_data.vocabulary_id,
            status="learning"
        )
        db.add(user_vocab)
        db.commit()
        db.refresh(user_vocab)

    # Update using SM-2 algorithm
    user_vocab = update_flashcard_review(
        user_vocab=user_vocab,
        quality=review_data.quality,
        db=db
    )

    # Create review record
    review = FlashcardReview(
        user_vocabulary_id=user_vocab.id,
        quality=review_data.quality,
        time_taken_seconds=review_data.time_taken_seconds,
        was_correct=review_data.quality >= 3
    )
    db.add(review)
    db.commit()

    return {"message": "Review submitted successfully", "next_review": user_vocab.next_review_date}


@router.get("/stats")
def get_vocabulary_stats(
    language_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get vocabulary learning statistics"""
    total = db.query(UserVocabulary).join(Vocabulary).filter(
        UserVocabulary.user_id == current_user.id,
        Vocabulary.language_id == language_id
    ).count()

    mastered = db.query(UserVocabulary).join(Vocabulary).filter(
        UserVocabulary.user_id == current_user.id,
        Vocabulary.language_id == language_id,
        UserVocabulary.status == "mastered"
    ).count()

    learning = db.query(UserVocabulary).join(Vocabulary).filter(
        UserVocabulary.user_id == current_user.id,
        Vocabulary.language_id == language_id,
        UserVocabulary.status == "learning"
    ).count()

    due_count = db.query(UserVocabulary).join(Vocabulary).filter(
        UserVocabulary.user_id == current_user.id,
        Vocabulary.language_id == language_id,
        UserVocabulary.next_review_date <= datetime.utcnow()
    ).count()

    return {
        "total_words": total,
        "mastered": mastered,
        "learning": learning,
        "due_for_review": due_count
    }

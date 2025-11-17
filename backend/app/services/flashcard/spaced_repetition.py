"""
Spaced Repetition Algorithm (SM-2)
Based on SuperMemo 2 algorithm
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.vocabulary import UserVocabulary


def calculate_next_interval(
    quality: int,
    ease_factor: float,
    interval: int,
    repetitions: int
) -> tuple[float, int, int]:
    """
    Calculate next review interval using SM-2 algorithm

    Args:
        quality: Quality of recall (0-5)
            0: Complete blackout
            1: Incorrect response; correct one remembered
            2: Incorrect response; correct one seemed easy to recall
            3: Correct response recalled with serious difficulty
            4: Correct response after hesitation
            5: Perfect response

        ease_factor: Easiness factor (minimum 1.3)
        interval: Current interval in days
        repetitions: Number of successful repetitions

    Returns:
        tuple: (new_ease_factor, new_interval, new_repetitions)
    """

    # Update ease factor
    new_ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))

    # Ensure ease factor is at least 1.3
    if new_ease_factor < 1.3:
        new_ease_factor = 1.3

    # Calculate new interval
    if quality < 3:
        # Failed recall - reset
        new_repetitions = 0
        new_interval = 1
    else:
        new_repetitions = repetitions + 1

        if new_repetitions == 1:
            new_interval = 1
        elif new_repetitions == 2:
            new_interval = 6
        else:
            new_interval = int(interval * new_ease_factor)

    return new_ease_factor, new_interval, new_repetitions


def update_flashcard_review(
    user_vocab: UserVocabulary,
    quality: int,
    db: Session
) -> UserVocabulary:
    """
    Update user vocabulary based on review quality

    Args:
        user_vocab: UserVocabulary instance
        quality: Quality rating (0-5)
        db: Database session

    Returns:
        Updated UserVocabulary instance
    """

    # Calculate new values using SM-2
    new_ease_factor, new_interval, new_repetitions = calculate_next_interval(
        quality=quality,
        ease_factor=user_vocab.ease_factor,
        interval=user_vocab.interval,
        repetitions=user_vocab.repetitions
    )

    # Update user vocabulary
    user_vocab.ease_factor = new_ease_factor
    user_vocab.interval = new_interval
    user_vocab.repetitions = new_repetitions
    user_vocab.last_reviewed_at = datetime.utcnow()
    user_vocab.next_review_date = datetime.utcnow() + timedelta(days=new_interval)
    user_vocab.times_reviewed += 1

    # Update counters
    if quality >= 3:
        user_vocab.times_correct += 1
    else:
        user_vocab.times_incorrect += 1

    # Update status
    if new_repetitions >= 5 and new_interval >= 21:
        user_vocab.status = "mastered"
        user_vocab.mastered_at = datetime.utcnow()
    elif new_repetitions > 0:
        user_vocab.status = "review"
    else:
        user_vocab.status = "learning"

    db.commit()
    db.refresh(user_vocab)

    return user_vocab


def get_daily_review_cards(
    user_id: int,
    language_id: int,
    max_new: int,
    max_review: int,
    db: Session
) -> dict:
    """
    Get cards for daily review session

    Args:
        user_id: User ID
        language_id: Language ID
        max_new: Maximum new cards
        max_review: Maximum review cards
        db: Database session

    Returns:
        Dictionary with new and review cards
    """
    from app.models.vocabulary import Vocabulary

    now = datetime.utcnow()

    # Get due review cards
    review_cards = db.query(UserVocabulary).join(Vocabulary).filter(
        UserVocabulary.user_id == user_id,
        Vocabulary.language_id == language_id,
        UserVocabulary.next_review_date <= now,
        UserVocabulary.status != "mastered"
    ).order_by(UserVocabulary.next_review_date).limit(max_review).all()

    # Get new cards
    learned_ids = db.query(UserVocabulary.vocabulary_id).filter(
        UserVocabulary.user_id == user_id
    ).all()
    learned_ids = [id[0] for id in learned_ids] if learned_ids else []

    new_cards_query = db.query(Vocabulary).filter(
        Vocabulary.language_id == language_id
    )

    if learned_ids:
        new_cards_query = new_cards_query.filter(~Vocabulary.id.in_(learned_ids))

    new_cards = new_cards_query.limit(max_new).all()

    return {
        "review_cards": review_cards,
        "new_cards": new_cards,
        "total_due": len(review_cards)
    }

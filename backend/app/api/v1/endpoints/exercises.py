from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.exercise import Exercise, ExerciseQuestion, UserExerciseHistory
from pydantic import BaseModel

router = APIRouter()


class ExerciseQuestionSchema(BaseModel):
    id: int
    question_text: str
    answer_data: dict
    explanation: Optional[str]
    order: int

    class Config:
        from_attributes = True


class ExerciseSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    difficulty: Optional[str]
    xp_reward: int
    estimated_time_minutes: Optional[int]
    questions: List[ExerciseQuestionSchema] = []

    class Config:
        from_attributes = True


class ExerciseSubmission(BaseModel):
    answers: dict  # question_id -> answer
    time_taken_seconds: int


@router.get("/", response_model=List[ExerciseSchema])
def get_exercises(
    language_id: int = Query(...),
    level_id: Optional[int] = None,
    exercise_type_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get available exercises"""
    query = db.query(Exercise).filter(
        Exercise.language_id == language_id,
        Exercise.is_active == True
    )

    if level_id:
        query = query.filter(Exercise.proficiency_level_id == level_id)

    if exercise_type_id:
        query = query.filter(Exercise.exercise_type_id == exercise_type_id)

    return query.offset(skip).limit(limit).all()


@router.get("/{exercise_id}", response_model=ExerciseSchema)
def get_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get specific exercise with questions"""
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    return exercise


@router.post("/{exercise_id}/submit")
def submit_exercise(
    exercise_id: int,
    submission: ExerciseSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Submit exercise answers and get results"""
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )

    # Get all questions
    questions = db.query(ExerciseQuestion).filter(
        ExerciseQuestion.exercise_id == exercise_id
    ).all()

    # Calculate score
    total_questions = len(questions)
    correct_answers = 0

    for question in questions:
        user_answer = submission.answers.get(str(question.id))
        correct_answer = question.answer_data.get("correct")

        if user_answer == correct_answer:
            correct_answers += 1

    score = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    xp_earned = int(exercise.xp_reward * (score / 100))

    # Save history
    history = UserExerciseHistory(
        user_id=current_user.id,
        exercise_id=exercise_id,
        score=score,
        total_questions=total_questions,
        correct_answers=correct_answers,
        time_taken_seconds=submission.time_taken_seconds,
        xp_earned=xp_earned,
        answers=submission.answers
    )
    db.add(history)
    db.commit()

    return {
        "score": score,
        "correct_answers": correct_answers,
        "total_questions": total_questions,
        "xp_earned": xp_earned,
        "percentage": score
    }


@router.get("/history/me")
def get_exercise_history(
    language_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get user's exercise history"""
    query = db.query(UserExerciseHistory).filter(
        UserExerciseHistory.user_id == current_user.id
    )

    if language_id:
        query = query.join(Exercise).filter(Exercise.language_id == language_id)

    return query.order_by(UserExerciseHistory.completed_at.desc()).offset(skip).limit(limit).all()

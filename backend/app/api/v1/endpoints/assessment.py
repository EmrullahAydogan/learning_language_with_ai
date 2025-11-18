"""
Level Assessment API endpoints
Provides endpoints for language proficiency level assessment
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.api import deps
from app.models.user import User
from app.models.language import Language, ProficiencyLevel
from app.models.assessment import LevelAssessment, AssessmentQuestion, AssessmentAnswer
from app.database import get_db

router = APIRouter()


# Schemas
class AssessmentQuestionResponse(BaseModel):
    id: int
    question_text: str
    question_type: str
    options: Optional[List[str]] = None
    order: int

    class Config:
        from_attributes = True


class StartAssessmentRequest(BaseModel):
    language_id: int


class StartAssessmentResponse(BaseModel):
    assessment_id: int
    language_name: str
    total_questions: int
    estimated_time_minutes: int
    questions: List[AssessmentQuestionResponse]


class SubmitAnswerRequest(BaseModel):
    question_id: int
    user_answer: str


class CompleteAssessmentResponse(BaseModel):
    level_code: str
    level_name: str
    score_percentage: float
    correct_answers: int
    total_questions: int
    recommendations: str


# Endpoints
@router.post("/start", response_model=StartAssessmentResponse)
def start_assessment(
    request: StartAssessmentRequest,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Start a new level assessment for a language
    """
    # Get language
    language = db.query(Language).filter(Language.id == request.language_id).first()
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")

    # Create assessment
    assessment = LevelAssessment(
        user_id=current_user.id,
        language_id=language.id,
        is_completed=False
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    # Get assessment questions for this language
    # Questions should be ordered by difficulty to assess level
    questions = db.query(AssessmentQuestion).filter(
        AssessmentQuestion.language_id == language.id,
        AssessmentQuestion.is_active == True
    ).order_by(AssessmentQuestion.order).limit(20).all()

    if not questions:
        raise HTTPException(
            status_code=404,
            detail="No assessment questions available for this language"
        )

    # Format questions for response
    question_responses = [
        AssessmentQuestionResponse(
            id=q.id,
            question_text=q.question_text,
            question_type=q.question_type,
            options=q.options if q.question_type == "multiple_choice" else None,
            order=q.order
        )
        for q in questions
    ]

    return StartAssessmentResponse(
        assessment_id=assessment.id,
        language_name=language.name,
        total_questions=len(questions),
        estimated_time_minutes=10,
        questions=question_responses
    )


@router.post("/{assessment_id}/answer")
def submit_answer(
    assessment_id: int,
    request: SubmitAnswerRequest,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit an answer for an assessment question
    """
    # Verify assessment belongs to user
    assessment = db.query(LevelAssessment).filter(
        LevelAssessment.id == assessment_id,
        LevelAssessment.user_id == current_user.id
    ).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    if assessment.is_completed:
        raise HTTPException(status_code=400, detail="Assessment already completed")

    # Get question
    question = db.query(AssessmentQuestion).filter(
        AssessmentQuestion.id == request.question_id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Check if answer is correct
    is_correct = question.correct_answer.lower().strip() == request.user_answer.lower().strip()

    # Save answer
    answer = AssessmentAnswer(
        assessment_id=assessment_id,
        question_id=request.question_id,
        user_answer=request.user_answer,
        is_correct=is_correct,
        time_spent_seconds=0  # Can be tracked on frontend
    )
    db.add(answer)
    db.commit()

    return {"is_correct": is_correct}


@router.post("/{assessment_id}/complete", response_model=CompleteAssessmentResponse)
def complete_assessment(
    assessment_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Complete the assessment and calculate proficiency level
    """
    # Get assessment
    assessment = db.query(LevelAssessment).filter(
        LevelAssessment.id == assessment_id,
        LevelAssessment.user_id == current_user.id
    ).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    if assessment.is_completed:
        raise HTTPException(status_code=400, detail="Assessment already completed")

    # Get all answers
    answers = db.query(AssessmentAnswer).filter(
        AssessmentAnswer.assessment_id == assessment_id
    ).all()

    if not answers:
        raise HTTPException(status_code=400, detail="No answers submitted")

    # Calculate score
    total_questions = len(answers)
    correct_answers = sum(1 for a in answers if a.is_correct)
    score_percentage = (correct_answers / total_questions) * 100

    # Determine proficiency level based on score
    level_code = "A1"  # Default
    recommendations = ""

    if score_percentage >= 90:
        level_code = "C1"
        recommendations = "Excellent! You have advanced proficiency. Focus on nuanced expressions and idiomatic usage."
    elif score_percentage >= 75:
        level_code = "B2"
        recommendations = "Great job! You have upper-intermediate proficiency. Work on complex grammar and advanced vocabulary."
    elif score_percentage >= 60:
        level_code = "B1"
        recommendations = "Good work! You have intermediate proficiency. Continue practicing conversation and reading."
    elif score_percentage >= 40:
        level_code = "A2"
        recommendations = "You're making progress! Focus on basic grammar and expanding your vocabulary."
    else:
        level_code = "A1"
        recommendations = "Start with the basics. Focus on common words, simple sentences, and everyday phrases."

    # Get level
    level = db.query(ProficiencyLevel).filter(
        ProficiencyLevel.code == level_code
    ).first()

    # Update assessment
    assessment.determined_level_id = level.id if level else None
    assessment.score_percentage = score_percentage
    assessment.correct_answers = correct_answers
    assessment.total_questions = total_questions
    assessment.is_completed = True
    db.commit()

    return CompleteAssessmentResponse(
        level_code=level_code,
        level_name=level.name if level else level_code,
        score_percentage=score_percentage,
        correct_answers=correct_answers,
        total_questions=total_questions,
        recommendations=recommendations
    )


@router.get("/history")
def get_assessment_history(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's assessment history
    """
    assessments = db.query(LevelAssessment).filter(
        LevelAssessment.user_id == current_user.id,
        LevelAssessment.is_completed == True
    ).all()

    return [{
        "id": a.id,
        "language_id": a.language_id,
        "level_code": a.determined_level.code if a.determined_level else None,
        "score_percentage": a.score_percentage,
        "completed_at": a.completed_at,
    } for a in assessments]

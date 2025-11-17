from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.writing import WritingSubmission, WritingEvaluation
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class SubmitWritingRequest(BaseModel):
    language_id: int
    prompt: Optional[str]
    topic: Optional[str]
    writing_type: str = "essay"
    title: Optional[str]
    content: str
    time_spent_seconds: Optional[int]


class WritingSubmissionSchema(BaseModel):
    id: int
    language_id: int
    prompt: Optional[str]
    topic: Optional[str]
    writing_type: str
    title: Optional[str]
    content: str
    word_count: Optional[int]
    submitted_at: datetime

    class Config:
        from_attributes = True


class WritingEvaluationSchema(BaseModel):
    id: int
    overall_score: Optional[float]
    grammar_score: Optional[float]
    vocabulary_score: Optional[float]
    coherence_score: Optional[float]
    grammar_errors: Optional[dict]
    vocabulary_suggestions: Optional[dict]
    ai_feedback: Optional[str]
    corrected_version: Optional[str]

    class Config:
        from_attributes = True


@router.post("/submit", response_model=WritingSubmissionSchema, status_code=status.HTTP_201_CREATED)
async def submit_writing(
    writing_data: SubmitWritingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Submit a writing for evaluation"""
    # Calculate word count
    word_count = len(writing_data.content.split())

    submission = WritingSubmission(
        user_id=current_user.id,
        language_id=writing_data.language_id,
        prompt=writing_data.prompt,
        topic=writing_data.topic,
        writing_type=writing_data.writing_type,
        title=writing_data.title,
        content=writing_data.content,
        word_count=word_count,
        time_spent_seconds=writing_data.time_spent_seconds
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    # Evaluate with AI
    from app.services.ai.openai_service import evaluate_writing

    evaluation_result = await evaluate_writing(
        content=writing_data.content,
        language_id=writing_data.language_id,
        writing_type=writing_data.writing_type
    )

    evaluation = WritingEvaluation(
        submission_id=submission.id,
        **evaluation_result
    )
    db.add(evaluation)
    db.commit()

    return submission


@router.get("/submissions", response_model=List[WritingSubmissionSchema])
def get_submissions(
    language_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get user's writing submissions"""
    query = db.query(WritingSubmission).filter(
        WritingSubmission.user_id == current_user.id
    )

    if language_id:
        query = query.filter(WritingSubmission.language_id == language_id)

    return query.order_by(WritingSubmission.submitted_at.desc()).offset(skip).limit(limit).all()


@router.get("/submissions/{submission_id}/evaluation", response_model=WritingEvaluationSchema)
def get_evaluation(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get evaluation for a submission"""
    submission = db.query(WritingSubmission).filter(
        WritingSubmission.id == submission_id,
        WritingSubmission.user_id == current_user.id
    ).first()

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )

    evaluation = db.query(WritingEvaluation).filter(
        WritingEvaluation.submission_id == submission_id
    ).first()

    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluation not found"
        )

    return evaluation

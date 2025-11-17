from typing import Any, List, Optional
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.speaking import SpeakingSession, SpeakingRecording
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class StartSessionRequest(BaseModel):
    language_id: int
    session_type: str = "conversation"
    scenario_name: Optional[str] = None
    difficulty_level: str = "medium"


class SpeakingSessionSchema(BaseModel):
    id: int
    language_id: int
    session_type: str
    scenario_name: Optional[str]
    overall_score: Optional[float]
    pronunciation_score: Optional[float]
    fluency_score: Optional[float]
    is_completed: bool
    started_at: datetime

    class Config:
        from_attributes = True


@router.post("/sessions", response_model=SpeakingSessionSchema, status_code=status.HTTP_201_CREATED)
def start_speaking_session(
    session_data: StartSessionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Start a new speaking practice session"""
    session = SpeakingSession(
        user_id=current_user.id,
        **session_data.dict()
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.post("/sessions/{session_id}/record")
async def upload_recording(
    session_id: int,
    audio: UploadFile = File(...),
    expected_text: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Upload audio recording for evaluation"""
    session = db.query(SpeakingSession).filter(
        SpeakingSession.id == session_id,
        SpeakingSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    # Save audio file
    from app.services.ai.speech_service import save_audio_file, transcribe_audio, evaluate_pronunciation

    audio_url = await save_audio_file(audio, current_user.id, session_id)

    # Transcribe
    transcription = await transcribe_audio(audio_url)

    # Evaluate
    scores = await evaluate_pronunciation(transcription, expected_text)

    # Save recording
    recording = SpeakingRecording(
        session_id=session_id,
        audio_url=audio_url,
        transcription=transcription,
        expected_text=expected_text,
        pronunciation_score=scores.get("pronunciation"),
        accuracy_score=scores.get("accuracy"),
        fluency_score=scores.get("fluency")
    )
    db.add(recording)
    db.commit()

    return {
        "transcription": transcription,
        "scores": scores,
        "recording_id": recording.id
    }


@router.get("/sessions", response_model=List[SpeakingSessionSchema])
def get_speaking_sessions(
    language_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get user's speaking sessions"""
    query = db.query(SpeakingSession).filter(
        SpeakingSession.user_id == current_user.id
    )

    if language_id:
        query = query.filter(SpeakingSession.language_id == language_id)

    return query.order_by(SpeakingSession.started_at.desc()).offset(skip).limit(limit).all()

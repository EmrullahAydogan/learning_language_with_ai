from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    users,
    languages,
    vocabulary,
    exercises,
    chat,
    speaking,
    reading,
    writing,
    progress,
    gamification,
    assessment,
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(languages.router, prefix="/languages", tags=["Languages"])
api_router.include_router(vocabulary.router, prefix="/vocabulary", tags=["Vocabulary"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["Exercises"])
api_router.include_router(assessment.router, prefix="/assessment", tags=["Assessment"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(speaking.router, prefix="/speaking", tags=["Speaking"])
api_router.include_router(reading.router, prefix="/reading", tags=["Reading"])
api_router.include_router(writing.router, prefix="/writing", tags=["Writing"])
api_router.include_router(progress.router, prefix="/progress", tags=["Progress"])
api_router.include_router(gamification.router, prefix="/gamification", tags=["Gamification"])

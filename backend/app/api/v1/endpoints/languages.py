from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.models.language import Language, ProficiencyLevel
from pydantic import BaseModel

router = APIRouter()


class LanguageSchema(BaseModel):
    id: int
    code: str
    name: str
    native_name: str
    flag: str
    is_active: bool

    class Config:
        from_attributes = True


class ProficiencyLevelSchema(BaseModel):
    id: int
    code: str
    name: str
    description: str

    class Config:
        from_attributes = True


@router.get("/", response_model=List[LanguageSchema])
def get_languages(
    db: Session = Depends(get_db)
) -> Any:
    """Get all available languages"""
    return db.query(Language).filter(Language.is_active == True).all()


@router.get("/levels", response_model=List[ProficiencyLevelSchema])
def get_proficiency_levels(
    db: Session = Depends(get_db)
) -> Any:
    """Get all proficiency levels"""
    return db.query(ProficiencyLevel).order_by(ProficiencyLevel.order).all()

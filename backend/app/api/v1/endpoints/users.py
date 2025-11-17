from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User, UserProfile, UserPreference, UserLanguage
from app.schemas.user import (
    User as UserSchema,
    UserUpdate,
    UserProfile as UserProfileSchema,
    UserProfileUpdate,
    UserPreference as UserPreferenceSchema,
    UserPreferenceUpdate,
    UserLanguage as UserLanguageSchema,
    UserLanguageCreate,
)

router = APIRouter()


@router.get("/me", response_model=UserSchema)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get current user information"""
    return current_user


@router.put("/me", response_model=UserSchema)
def update_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Update current user"""
    if user_update.email:
        existing = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        current_user.email = user_update.email

    if user_update.username:
        existing = db.query(User).filter(
            User.username == user_update.username,
            User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        current_user.username = user_update.username

    if user_update.password:
        from app.core.security import get_password_hash
        current_user.hashed_password = get_password_hash(user_update.password)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/me/profile", response_model=UserProfileSchema)
def get_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get current user profile"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        # Create if doesn't exist
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


@router.put("/me/profile", response_model=UserProfileSchema)
def update_user_profile(
    profile_update: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Update current user profile"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile


@router.get("/me/preferences", response_model=UserPreferenceSchema)
def get_user_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get current user preferences"""
    preferences = db.query(UserPreference).filter(
        UserPreference.user_id == current_user.id
    ).first()
    if not preferences:
        preferences = UserPreference(user_id=current_user.id)
        db.add(preferences)
        db.commit()
        db.refresh(preferences)
    return preferences


@router.put("/me/preferences", response_model=UserPreferenceSchema)
def update_user_preferences(
    preferences_update: UserPreferenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Update current user preferences"""
    preferences = db.query(UserPreference).filter(
        UserPreference.user_id == current_user.id
    ).first()
    if not preferences:
        preferences = UserPreference(user_id=current_user.id)
        db.add(preferences)

    update_data = preferences_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(preferences, field, value)

    db.commit()
    db.refresh(preferences)
    return preferences


@router.get("/me/languages", response_model=list[UserLanguageSchema])
def get_user_languages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get user's languages"""
    return db.query(UserLanguage).filter(UserLanguage.user_id == current_user.id).all()


@router.post("/me/languages", response_model=UserLanguageSchema, status_code=status.HTTP_201_CREATED)
def add_user_language(
    language_data: UserLanguageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Add a language for the user"""
    existing = db.query(UserLanguage).filter(
        UserLanguage.user_id == current_user.id,
        UserLanguage.language_id == language_data.language_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Language already added"
        )

    user_language = UserLanguage(
        user_id=current_user.id,
        **language_data.dict()
    )
    db.add(user_language)
    db.commit()
    db.refresh(user_language)
    return user_language

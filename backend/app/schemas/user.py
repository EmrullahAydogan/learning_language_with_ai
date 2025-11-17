from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class User(UserInDB):
    pass


# User Profile Schemas
class UserProfileBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    native_language_id: Optional[int] = None
    timezone: Optional[str] = "UTC"


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    pass


class UserProfile(UserProfileBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# User Language Schemas
class UserLanguageBase(BaseModel):
    language_id: int
    proficiency_level_id: int
    target_level_id: Optional[int] = None
    is_primary: bool = False


class UserLanguageCreate(UserLanguageBase):
    pass


class UserLanguage(UserLanguageBase):
    id: int
    user_id: int
    started_at: datetime

    class Config:
        from_attributes = True


# User Preference Schemas
class UserPreferenceBase(BaseModel):
    daily_goal_minutes: Optional[int] = 15
    daily_goal_xp: Optional[int] = 50
    new_words_per_day: Optional[int] = 10
    email_notifications: Optional[bool] = True
    push_notifications: Optional[bool] = True
    reminder_time: Optional[str] = None
    difficulty_preference: Optional[str] = "adaptive"
    audio_speed: Optional[int] = 100
    show_translation: Optional[bool] = True
    theme: Optional[str] = "light"


class UserPreferenceUpdate(UserPreferenceBase):
    pass


class UserPreference(UserPreferenceBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

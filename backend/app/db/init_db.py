from sqlalchemy.orm import Session
from app.models.language import Language, ProficiencyLevel
from app.models.vocabulary import VocabularyCategory
from app.models.exercise import ExerciseType
from app.core.security import get_password_hash


def init_db(db: Session) -> None:
    """Initialize database with default data"""

    # Create proficiency levels
    levels = [
        {"code": "A1", "name": "Beginner", "description": "Can understand and use familiar everyday expressions"},
        {"code": "A2", "name": "Elementary", "description": "Can communicate in simple and routine tasks"},
        {"code": "B1", "name": "Intermediate", "description": "Can deal with most situations while traveling"},
        {"code": "B2", "name": "Upper Intermediate", "description": "Can interact with a degree of fluency"},
        {"code": "C1", "name": "Advanced", "description": "Can express ideas fluently and spontaneously"},
        {"code": "C2", "name": "Proficient", "description": "Can understand virtually everything"},
    ]

    for level_data in levels:
        level = db.query(ProficiencyLevel).filter(
            ProficiencyLevel.code == level_data["code"]
        ).first()
        if not level:
            level = ProficiencyLevel(**level_data)
            db.add(level)

    # Create languages
    languages = [
        {"code": "en", "name": "English", "native_name": "English", "flag": "🇬🇧"},
        {"code": "es", "name": "Spanish", "native_name": "Español", "flag": "🇪🇸"},
        {"code": "fr", "name": "French", "native_name": "Français", "flag": "🇫🇷"},
        {"code": "de", "name": "German", "native_name": "Deutsch", "flag": "🇩🇪"},
        {"code": "it", "name": "Italian", "native_name": "Italiano", "flag": "🇮🇹"},
        {"code": "tr", "name": "Turkish", "native_name": "Türkçe", "flag": "🇹🇷"},
    ]

    for lang_data in languages:
        language = db.query(Language).filter(
            Language.code == lang_data["code"]
        ).first()
        if not language:
            language = Language(**lang_data)
            db.add(language)

    # Create vocabulary categories
    categories = [
        "Daily Life", "Food & Drink", "Travel", "Work & Business",
        "Health", "Education", "Technology", "Sports & Hobbies",
        "Family & Relationships", "Shopping", "Weather", "Emotions",
        "Colors", "Numbers", "Time", "Directions", "Animals", "Nature"
    ]

    for cat_name in categories:
        category = db.query(VocabularyCategory).filter(
            VocabularyCategory.name == cat_name
        ).first()
        if not category:
            category = VocabularyCategory(name=cat_name)
            db.add(category)

    # Create exercise types
    exercise_types = [
        {"name": "Multiple Choice", "code": "mcq", "description": "Choose the correct answer"},
        {"name": "Fill in the Blank", "code": "fill_blank", "description": "Complete the sentence"},
        {"name": "True/False", "code": "true_false", "description": "Determine if statement is correct"},
        {"name": "Matching", "code": "matching", "description": "Match items together"},
        {"name": "Ordering", "code": "ordering", "description": "Put items in correct order"},
        {"name": "Translation", "code": "translation", "description": "Translate text"},
        {"name": "Listening", "code": "listening", "description": "Listen and answer"},
        {"name": "Reading", "code": "reading", "description": "Read and comprehend"},
    ]

    for et_data in exercise_types:
        ex_type = db.query(ExerciseType).filter(
            ExerciseType.code == et_data["code"]
        ).first()
        if not ex_type:
            ex_type = ExerciseType(**et_data)
            db.add(ex_type)

    db.commit()

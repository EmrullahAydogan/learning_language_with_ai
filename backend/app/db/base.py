"""Import all models here for Alembic to detect them"""

from app.db.session import Base  # noqa
from app.models.user import User, UserProfile, UserLanguage, UserPreference  # noqa
from app.models.language import Language, ProficiencyLevel  # noqa
from app.models.vocabulary import (  # noqa
    Vocabulary,
    VocabularyCategory,
    UserVocabulary,
    FlashcardReview
)
from app.models.exercise import (  # noqa
    Exercise,
    ExerciseType,
    ExerciseQuestion,
    UserExerciseHistory
)
from app.models.lesson import Lesson, Topic  # noqa
from app.models.chat import ChatConversation, ChatMessage  # noqa
from app.models.speaking import SpeakingSession, SpeakingRecording, SpeakingEvaluation  # noqa
from app.models.reading import ReadingMaterial, UserReadingHistory  # noqa
from app.models.writing import WritingSubmission, WritingEvaluation  # noqa
from app.models.progress import (  # noqa
    UserProgress,
    DailyActivity,
    Streak,
    UserXP,
    UserLevel
)
from app.models.gamification import (  # noqa
    Achievement,
    Badge,
    UserAchievement,
    Challenge,
    UserChallenge
)
from app.models.assessment import (  # noqa
    LevelAssessment,
    AssessmentQuestion,
    AssessmentAnswer
)

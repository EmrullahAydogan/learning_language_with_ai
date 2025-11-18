"""
Text-to-Speech service using OpenAI TTS API
"""

from typing import Optional, BinaryIO
from pathlib import Path
import hashlib
from openai import OpenAI
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class TTSService:
    """Text-to-Speech service using OpenAI"""

    # Language code to voice mapping
    VOICE_MAPPING = {
        "en": "alloy",  # English - neutral voice
        "es": "nova",   # Spanish - warm voice
        "fr": "shimmer",  # French - expressive voice
        "de": "fable",  # German - British accent
        "it": "onyx",   # Italian - deep voice
        "tr": "alloy",  # Turkish - use alloy as default
    }

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.cache_dir = Path(settings.UPLOAD_DIR) / "tts_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, text: str, language_code: str, voice: str) -> Path:
        """Generate cache file path based on content hash"""
        content = f"{text}_{language_code}_{voice}"
        file_hash = hashlib.md5(content.encode()).hexdigest()
        return self.cache_dir / f"{file_hash}.mp3"

    def _is_cached(self, text: str, language_code: str, voice: str) -> bool:
        """Check if audio is already cached"""
        cache_path = self._get_cache_path(text, language_code, voice)
        return cache_path.exists()

    def generate_speech(
        self,
        text: str,
        language_code: str,
        voice: Optional[str] = None,
        use_cache: bool = True
    ) -> Optional[Path]:
        """
        Generate speech audio from text

        Args:
            text: Text to convert to speech
            language_code: Language code (en, es, fr, de, it, tr)
            voice: Optional voice name. If not provided, uses language default
            use_cache: Whether to use cached audio if available

        Returns:
            Path to audio file or None if generation failed
        """
        # Select voice based on language if not provided
        if voice is None:
            voice = self.VOICE_MAPPING.get(language_code, "alloy")

        # Check cache
        cache_path = self._get_cache_path(text, language_code, voice)
        if use_cache and cache_path.exists():
            logger.info(f"Using cached TTS audio: {cache_path}")
            return cache_path

        try:
            # Generate audio using OpenAI TTS
            logger.info(f"Generating TTS audio for text: {text[:50]}...")

            response = self.client.audio.speech.create(
                model="tts-1",  # Use tts-1-hd for higher quality
                voice=voice,
                input=text,
                speed=1.0  # Normal speed, can be 0.25 to 4.0
            )

            # Save to cache
            response.stream_to_file(cache_path)
            logger.info(f"TTS audio generated and cached: {cache_path}")

            return cache_path

        except Exception as e:
            logger.error(f"Failed to generate TTS audio: {e}")
            return None

    def generate_pronunciation(
        self,
        word: str,
        language_code: str,
        voice: Optional[str] = None
    ) -> Optional[Path]:
        """
        Generate pronunciation audio for a single word

        Args:
            word: Word to pronounce
            language_code: Language code
            voice: Optional voice name

        Returns:
            Path to audio file or None if generation failed
        """
        return self.generate_speech(
            text=word,
            language_code=language_code,
            voice=voice,
            use_cache=True
        )

    def generate_sentence_audio(
        self,
        sentence: str,
        language_code: str,
        voice: Optional[str] = None
    ) -> Optional[Path]:
        """
        Generate audio for an example sentence

        Args:
            sentence: Sentence to convert to speech
            language_code: Language code
            voice: Optional voice name

        Returns:
            Path to audio file or None if generation failed
        """
        return self.generate_speech(
            text=sentence,
            language_code=language_code,
            voice=voice,
            use_cache=True
        )

    def clear_cache(self, max_age_days: int = 30) -> int:
        """
        Clear old cached audio files

        Args:
            max_age_days: Remove files older than this many days

        Returns:
            Number of files removed
        """
        import time
        removed_count = 0
        current_time = time.time()
        max_age_seconds = max_age_days * 24 * 60 * 60

        for audio_file in self.cache_dir.glob("*.mp3"):
            file_age = current_time - audio_file.stat().st_mtime
            if file_age > max_age_seconds:
                audio_file.unlink()
                removed_count += 1

        logger.info(f"Cleared {removed_count} old TTS cache files")
        return removed_count

    def get_available_voices(self) -> dict:
        """Get list of available voices per language"""
        return {
            "en": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
            "es": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
            "fr": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
            "de": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
            "it": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
            "tr": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
        }


# Singleton instance
tts_service = TTSService()

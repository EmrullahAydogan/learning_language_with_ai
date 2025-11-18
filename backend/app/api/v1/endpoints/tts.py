"""
Text-to-Speech API endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from app.services.tts import tts_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class TTSRequest(BaseModel):
    text: str
    language_code: str = "en"
    voice: Optional[str] = None


@router.post("/generate")
def generate_tts_audio(request: TTSRequest):
    """
    Generate speech audio from text

    - **text**: Text to convert to speech
    - **language_code**: Language code (en, es, fr, de, it, tr)
    - **voice**: Optional voice name (alloy, echo, fable, onyx, nova, shimmer)
    """
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    if len(request.text) > 4096:
        raise HTTPException(status_code=400, detail="Text is too long (max 4096 characters)")

    try:
        audio_path = tts_service.generate_speech(
            text=request.text,
            language_code=request.language_code,
            voice=request.voice
        )

        if not audio_path or not audio_path.exists():
            raise HTTPException(status_code=500, detail="Failed to generate audio")

        return FileResponse(
            path=audio_path,
            media_type="audio/mpeg",
            filename=f"speech_{audio_path.stem}.mp3"
        )

    except Exception as e:
        logger.error(f"TTS generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate audio: {str(e)}")


@router.get("/pronunciation/{word}")
def get_word_pronunciation(
    word: str,
    language_code: str = Query("en", description="Language code"),
    voice: Optional[str] = Query(None, description="Voice name")
):
    """
    Get pronunciation audio for a specific word

    - **word**: Word to pronounce
    - **language_code**: Language code (en, es, fr, de, it, tr)
    - **voice**: Optional voice name
    """
    if not word or len(word.strip()) == 0:
        raise HTTPException(status_code=400, detail="Word cannot be empty")

    if len(word) > 100:
        raise HTTPException(status_code=400, detail="Word is too long")

    try:
        audio_path = tts_service.generate_pronunciation(
            word=word,
            language_code=language_code,
            voice=voice
        )

        if not audio_path or not audio_path.exists():
            raise HTTPException(status_code=500, detail="Failed to generate pronunciation")

        return FileResponse(
            path=audio_path,
            media_type="audio/mpeg",
            filename=f"pronunciation_{word}.mp3"
        )

    except Exception as e:
        logger.error(f"Pronunciation generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate pronunciation: {str(e)}")


@router.get("/voices")
def get_available_voices():
    """
    Get list of available TTS voices per language

    Returns a dictionary mapping language codes to available voice names
    """
    return tts_service.get_available_voices()


@router.delete("/cache")
def clear_tts_cache(max_age_days: int = Query(30, description="Remove files older than this many days")):
    """
    Clear old cached TTS audio files

    - **max_age_days**: Remove files older than this many days (default: 30)

    Returns the number of files removed
    """
    try:
        removed_count = tts_service.clear_cache(max_age_days=max_age_days)
        return {
            "message": f"Cleared {removed_count} old TTS cache files",
            "removed_count": removed_count
        }
    except Exception as e:
        logger.error(f"Cache clearing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")

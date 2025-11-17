"""
Speech recognition and text-to-speech services using OpenAI Whisper
"""
import openai
from typing import Optional, Dict, Any
from fastapi import UploadFile
import os
from datetime import datetime
from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY


async def save_audio_file(
    audio: UploadFile,
    user_id: int,
    session_id: int
) -> str:
    """Save uploaded audio file"""

    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(settings.UPLOAD_DIR, "audio", str(user_id))
    os.makedirs(upload_dir, exist_ok=True)

    # Generate unique filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"session_{session_id}_{timestamp}.webm"
    file_path = os.path.join(upload_dir, filename)

    # Save file
    with open(file_path, "wb") as f:
        content = await audio.read()
        f.write(content)

    # Return relative path
    return f"/uploads/audio/{user_id}/{filename}"


async def transcribe_audio(audio_path: str) -> str:
    """Transcribe audio using OpenAI Whisper"""

    try:
        # Convert relative path to absolute
        full_path = os.path.join(os.getcwd(), audio_path.lstrip("/"))

        with open(full_path, "rb") as audio_file:
            transcript = await openai.Audio.atranscribe(
                model="whisper-1",
                file=audio_file
            )

        return transcript.text

    except Exception as e:
        print(f"Transcription error: {e}")
        return ""


async def evaluate_pronunciation(
    transcription: str,
    expected_text: Optional[str] = None
) -> Dict[str, float]:
    """Evaluate pronunciation quality"""

    if not transcription:
        return {
            "pronunciation": 0,
            "accuracy": 0,
            "fluency": 0
        }

    # If we have expected text, compare accuracy
    if expected_text:
        # Simple word-level comparison
        transcribed_words = transcription.lower().split()
        expected_words = expected_text.lower().split()

        if len(expected_words) > 0:
            # Calculate accuracy based on matching words
            matches = sum(1 for t, e in zip(transcribed_words, expected_words) if t == e)
            accuracy = (matches / len(expected_words)) * 100
        else:
            accuracy = 0
    else:
        # Without expected text, we can't measure accuracy precisely
        accuracy = 70  # Default score

    # Use AI to evaluate overall quality
    try:
        prompt = f"""Evaluate the following transcribed speech for pronunciation and fluency.

Transcription: {transcription}
{f'Expected: {expected_text}' if expected_text else ''}

Rate on a scale of 0-100:
1. Pronunciation quality
2. Fluency
3. Overall accuracy

Return as JSON: {{"pronunciation": X, "fluency": Y, "accuracy": Z}}
"""

        response = await openai.ChatCompletion.acreate(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        import json
        scores = json.loads(response.choices[0].message.content)

        return {
            "pronunciation": scores.get("pronunciation", 70),
            "fluency": scores.get("fluency", 70),
            "accuracy": scores.get("accuracy", accuracy)
        }

    except Exception as e:
        print(f"Evaluation error: {e}")
        return {
            "pronunciation": 70,
            "accuracy": accuracy,
            "fluency": 70
        }


async def text_to_speech(text: str, language: str = "en") -> bytes:
    """Convert text to speech using OpenAI TTS"""

    try:
        response = await openai.Audio.create_speech(
            model="tts-1",
            voice="alloy",
            input=text
        )

        return response.content

    except Exception as e:
        print(f"TTS error: {e}")
        return b""

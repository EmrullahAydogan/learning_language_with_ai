"""
OpenAI GPT-4 integration for chat, evaluation, and content generation
"""
import openai
from typing import Optional, Dict, Any, List, Tuple
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.chat import ChatMessage

openai.api_key = settings.OPENAI_API_KEY


def get_initial_chat_prompt(
    conversation_type: str,
    scenario: Optional[str] = None,
    character: Optional[str] = "friendly_tutor"
) -> str:
    """Generate initial system prompt for chat conversation"""

    base_prompts = {
        "friendly_tutor": "You are a friendly and encouraging language tutor. Help the user practice the language naturally, correct their mistakes gently, and provide helpful explanations.",
        "strict_teacher": "You are a strict but fair language teacher. Focus on accuracy and correct all mistakes immediately. Provide detailed grammar explanations.",
        "native_speaker": "You are a native speaker having a casual conversation. Speak naturally and help the user understand colloquial expressions and cultural context.",
        "professional": "You are a professional language instructor. Provide structured lessons and systematic feedback."
    }

    scenario_prompts = {
        "restaurant": "We are role-playing a restaurant scenario. You are a waiter/waitress. Help the user practice ordering food, asking questions about the menu, and making requests.",
        "airport": "We are role-playing an airport scenario. You are an airline staff member. Help the user practice check-in, asking about flights, and handling travel situations.",
        "job_interview": "We are role-playing a job interview. You are the interviewer. Ask professional questions and help the user practice formal language.",
        "shopping": "We are role-playing a shopping scenario. You are a shop assistant. Help the user practice asking about products, prices, and making purchases.",
        "doctor": "We are role-playing a medical scenario. You are a doctor. Help the user practice describing symptoms and understanding medical advice."
    }

    prompt = base_prompts.get(character, base_prompts["friendly_tutor"])

    if conversation_type == "scenario" and scenario:
        prompt += "\n\n" + scenario_prompts.get(scenario, "")

    prompt += "\n\nAlways respond in the language being learned. Keep responses natural and conversational."

    return prompt


async def get_chat_response(
    conversation_id: int,
    user_message: str,
    db: Session
) -> Tuple[str, Optional[Dict]]:
    """Get AI response for chat message"""

    # Get conversation history
    messages = db.query(ChatMessage).filter(
        ChatMessage.conversation_id == conversation_id
    ).order_by(ChatMessage.created_at).all()

    # Prepare messages for OpenAI
    openai_messages = []
    for msg in messages:
        if msg.role in ["system", "user", "assistant"]:
            openai_messages.append({
                "role": msg.role,
                "content": msg.content
            })

    # Add current user message
    openai_messages.append({
        "role": "user",
        "content": user_message
    })

    try:
        # Call OpenAI API
        response = await openai.ChatCompletion.acreate(
            model=settings.OPENAI_MODEL,
            messages=openai_messages,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS
        )

        ai_response = response.choices[0].message.content

        # Optionally analyze user message for corrections
        corrections = await analyze_message_for_errors(user_message)

        return ai_response, corrections

    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "I'm sorry, I'm having trouble connecting right now. Please try again.", None


async def analyze_message_for_errors(message: str) -> Optional[Dict]:
    """Analyze user message for grammar/spelling errors"""

    prompt = f"""Analyze the following text for grammar, spelling, and usage errors.
Return a JSON object with corrections, or null if there are no errors.

Text: {message}

Format:
{{
    "has_errors": true/false,
    "corrections": [
        {{"original": "...", "corrected": "...", "explanation": "..."}}
    ]
}}
"""

    try:
        response = await openai.ChatCompletion.acreate(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        import json
        result = json.loads(response.choices[0].message.content)
        return result if result.get("has_errors") else None

    except:
        return None


async def evaluate_writing(
    content: str,
    language_id: int,
    writing_type: str
) -> Dict[str, Any]:
    """Evaluate writing submission using AI"""

    prompt = f"""Evaluate the following {writing_type} and provide detailed feedback.

Text:
{content}

Please provide:
1. Overall score (0-100)
2. Grammar score (0-100)
3. Vocabulary score (0-100)
4. Coherence score (0-100)
5. Style score (0-100)
6. Grammar errors with corrections
7. Vocabulary improvement suggestions
8. Overall feedback
9. A corrected version of the text

Return as JSON.
"""

    try:
        response = await openai.ChatCompletion.acreate(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=2000
        )

        import json
        result = json.loads(response.choices[0].message.content)

        return {
            "overall_score": result.get("overall_score", 0),
            "grammar_score": result.get("grammar_score", 0),
            "vocabulary_score": result.get("vocabulary_score", 0),
            "coherence_score": result.get("coherence_score", 0),
            "style_score": result.get("style_score", 0),
            "grammar_errors": result.get("grammar_errors", []),
            "vocabulary_suggestions": result.get("vocabulary_suggestions", []),
            "ai_feedback": result.get("feedback", ""),
            "corrected_version": result.get("corrected_version", "")
        }

    except Exception as e:
        print(f"Writing evaluation error: {e}")
        return {
            "overall_score": 0,
            "grammar_score": 0,
            "vocabulary_score": 0,
            "coherence_score": 0,
            "style_score": 0,
            "grammar_errors": [],
            "vocabulary_suggestions": [],
            "ai_feedback": "Unable to evaluate at this time.",
            "corrected_version": content
        }


async def generate_exercise_content(
    language_id: int,
    level_id: int,
    topic: str,
    exercise_type: str
) -> Dict[str, Any]:
    """Generate exercise content using AI"""

    prompt = f"""Create a {exercise_type} exercise for language learning.

Topic: {topic}
Level: {level_id}

Generate 5-10 questions appropriate for this level.
Return as JSON with questions and answers.
"""

    try:
        response = await openai.ChatCompletion.acreate(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        import json
        return json.loads(response.choices[0].message.content)

    except Exception as e:
        print(f"Exercise generation error: {e}")
        return {"questions": []}

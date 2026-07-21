"""
chatbot.py
Handles the connection to the Gemini API and generates chatbot replies.
Uses the current `google-genai` SDK (the old `google-generativeai`
package is deprecated and no longer receives updates).
"""

import os
from google import genai

from prompt import build_prompt

# Model name is configurable via .env so you can switch versions
# without touching code. Falls back to a sensible default.
DEFAULT_MODEL = "gemini-3.1-flash-lite"
_client = None


def _get_client():
    """Lazily create and cache the Gemini client instance."""
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GEMINI_API_KEY not found. Make sure it's set in your .env file."
            )
        _client = genai.Client(api_key=api_key)
    return _client


def get_response(user_query: str, context: str, history: list | None = None) -> str:
    """
    Generate a chatbot reply grounded in the hotel's data.

    Args:
        user_query: The guest's message.
        context: Formatted hotel knowledge base text.
        history: Optional list of (user, bot) tuples for multi-turn memory.

    Returns:
        The chatbot's reply as a string.
    """
    if not user_query or not user_query.strip():
        return "Could you tell me a bit more about what you'd like to know?"

    prompt = build_prompt(user_query, context, history)

    try:
        client = _get_client()
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
        )
        text = (response.text or "").strip()
        return text if text else "Sorry, I couldn't find an answer for that question."
    except EnvironmentError as e:
        return f"Configuration error: {e}"

    except Exception as e:
        print("Gemini Error:", e)

        return (
            "⚠️ Our AI Concierge is currently unavailable. "
            "Please try again in a few moments."
        )
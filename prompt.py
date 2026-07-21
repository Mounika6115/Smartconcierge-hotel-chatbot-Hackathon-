"""
prompt.py
Builds the system + user prompt sent to the Gemini model.
Keeping this separate makes it easy to tune the chatbot's tone
and behavior without touching the API-calling logic.
"""

SYSTEM_INSTRUCTIONS = """You are Dusyanth Chinni AI Concierge, the official AI assistant of Dusyanth Chinni Hotel & Spa.

Rules you must follow:
1. Answer ONLY using the hotel information provided in the CONTEXT section below.
2. If the answer is not contained in the CONTEXT, politely say you don't have
   that information and suggest the guest contact the front desk.
3. Keep answers concise, warm, and helpful — like a real hotel concierge.
4. Never invent prices, policies, or amenities that are not in the CONTEXT.
5. If the guest asks something unrelated to the hotel (e.g. general trivia),
   gently steer the conversation back to how you can help with their stay.
"""


def build_prompt(user_query: str, context: str, history: list | None = None) -> str:
    """
    Assemble the full prompt to send to Gemini.

    Args:
        user_query: The guest's latest message.
        context: Formatted hotel data (from data_loader.format_context).
        history: Optional list of (user, bot) tuples for conversation memory.
    """
    history_block = ""
    if history:
        formatted_turns = []
        for user_msg, bot_msg in history[-5:]:  # keep last 5 turns for brevity
            formatted_turns.append(f"Guest: {user_msg}\nSmartConcierge: {bot_msg}")
        history_block = "\n\nCONVERSATION HISTORY:\n" + "\n".join(formatted_turns)

    prompt = f"""{SYSTEM_INSTRUCTIONS}

CONTEXT (hotel information):
{context}
{history_block}

Guest: {user_query}
SmartConcierge:"""

    return prompt
"""
app.py
Entry point for SmartConcierge - Hotel Chatbot.
Run this file to start an interactive chat session in the terminal.
"""

from dotenv import load_dotenv

from data_loader import load_data, format_context
from chatbot import get_response

DATA_FILE = "hotel_chatbot_data.json"


def main():
    load_dotenv()  # reads GEMINI_API_KEY (and GEMINI_MODEL) from .env

    try:
        hotel_data = load_data(DATA_FILE)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    context = format_context(hotel_data)
    hotel_name = hotel_data.get("hotel_name", "our hotel")

    print(f"Bot: Welcome to {hotel_name}! I'm SmartConcierge, your virtual assistant.")
    print("Bot: Ask me about rooms, amenities, policies, or anything about your stay.")
    print("Bot: Type 'exit' or 'quit' to end the chat.\n")

    history = []

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ("exit", "quit"):
            print("Bot: Thank you for chatting with SmartConcierge. Have a great stay!")
            break

        reply = get_response(user_input, context, history)
        print(f"Bot: {reply}\n")

        history.append((user_input, reply))


if __name__ == "__main__":
    main()
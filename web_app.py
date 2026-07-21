"""
web_app.py
Runs SmartConcierge as a web app you can open in a browser.
Your existing app.py (terminal version) still works separately —
this just adds a branded browser front-end on top of the same chatbot logic.
"""

from datetime import datetime

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from data_loader import load_data, format_context
from chatbot import get_response

load_dotenv()

app = Flask(__name__)

DATA_FILE = "hotel_chatbot_data.json"

# Load hotel data once at startup
hotel_data = load_data(DATA_FILE)
context = format_context(hotel_data)
hotel_name = hotel_data.get("hotel_name", "our hotel")

# --- Branding / display config -------------------------------------------
# Edit these to match your property. In a larger project these could move
# into hotel_chatbot_data.json instead of living here.
BRANDING = {
    "hotel_name": hotel_name,
    "assistant_name": "Dusyanth Chinni AI Concierge",
    "tagline": "Luxury • Comfort • Memorable Stays",
    "location": "Hyderabad, Telangana, India",
    "star_rating": "★★★★★ Luxury Hotel",
    "reception_hours": "Reception Open 24/7",
    "contact_phone": "+91 98987 26532",
    "contact_email": "contact@dchotel.com",
    "website": "www.dusyanthchinnihotel.com",
    "welcome_message": (
    "Welcome to Dusyanth Chinni Hotel & Spa!\n\n"
    "I'm your AI Concierge.\n\n"
    "I can help you with:\n"
    "• Room Booking\n"
    "• Room Information\n"
    "• Restaurant & Dining\n"
    "• Spa & Wellness\n"
    "• Airport Pickup\n"
    "• Nearby Attractions\n"
    "• Personalized Recommendations\n\n"
    "How may I assist you today?"

    ),
    "quick_actions": [
        "Room types",
        "Check room availability",
        "Room prices",
        "Restaurant menu",
        "Spa & wellness",
        "Swimming pool",
        "Airport pickup",
        "Nearby attractions",
        "Check-in & check-out",
        "Contact reception",
    ],
}

# Simple in-memory history (per server run — resets if you restart)
# Good enough for a hackathon demo; not per-user/session.
chat_history = []


@app.route("/")
def index():
    return render_template(
        "index.html",
        current_year=datetime.now().year,
        **BRANDING,
    )


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a question."})

    reply = get_response(user_message, context, chat_history)
    chat_history.append((user_message, reply))

    return jsonify({"reply": reply})


@app.route("/api/reset", methods=["POST"])
def reset():
    chat_history.clear()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print(f"\nSmartConcierge web app running for {hotel_name}")
    app.run(host="0.0.0.0", port=5000)
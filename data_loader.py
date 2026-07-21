"""
data_loader.py
Loads the hotel's knowledge base (JSON) and formats it into a
plain-text context block the LLM can use to answer questions.

Supports two JSON shapes:
1. The original sample shape: hotel_name, location, contact, rooms,
   amenities, policies, faqs (list of {question, answer}).
2. The category-based FAQ shape: hotel_name, faq (list of
   {category, question, answer}).
Both can be present at once — the function includes whatever it finds.
"""

import json
import os


def load_data(filepath: str = "hotel_chatbot_data.json") -> dict:
    """Load hotel data from a JSON file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find data file: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def format_context(data: dict) -> str:
    """
    Convert the hotel JSON data into a readable text block.
    This text is injected into the prompt as grounding context
    so the model answers using real hotel info instead of guessing.
    """
    lines = []

    lines.append(f"Hotel Name: {data.get('hotel_name', 'N/A')}")

    if data.get("location"):
        lines.append(f"Location: {data['location']}")

    contact = data.get("contact", {})
    if contact:
        lines.append(f"Contact: Phone {contact.get('phone', 'N/A')}, "
                      f"Email {contact.get('email', 'N/A')}")

    if data.get("check_in_time"):
        lines.append(f"Check-in Time: {data['check_in_time']}")
    if data.get("check_out_time"):
        lines.append(f"Check-out Time: {data['check_out_time']}")

    rooms = data.get("rooms", [])
    if rooms:
        lines.append("\nRoom Types:")
        for room in rooms:
            lines.append(
                f"- {room['type']}: ${room['price_per_night']}/night, "
                f"sleeps {room['capacity']}, amenities: {', '.join(room['amenities'])}"
            )

    amenities = data.get("amenities", [])
    if amenities:
        lines.append("\nHotel Amenities:")
        for amenity in amenities:
            lines.append(f"- {amenity}")

    policies = data.get("policies", {})
    if policies:
        lines.append("\nPolicies:")
        for key, value in policies.items():
            lines.append(f"- {key.capitalize()}: {value}")

    # --- Original simple FAQ shape: "faqs": [{question, answer}] ---
    simple_faqs = data.get("faqs", [])
    if simple_faqs:
        lines.append("\nFrequently Asked Questions:")
        for faq in simple_faqs:
            lines.append(f"- Q: {faq['question']}\n  A: {faq['answer']}")

    # --- Category-based FAQ shape: "faq": [{category, question, answer}] ---
    categorized_faqs = data.get("faq", [])
    if categorized_faqs:
        grouped = {}
        for item in categorized_faqs:
            category = item.get("category", "General")
            grouped.setdefault(category, []).append(item)

        lines.append("\nFrequently Asked Questions:")
        for category, items in grouped.items():
            lines.append(f"\n[{category}]")
            for item in items:
                lines.append(f"- Q: {item['question']}\n  A: {item['answer']}")

    return "\n".join(lines)


if __name__ == "__main__":
    # Quick manual test: python data_loader.py
    data = load_data()
    print(format_context(data))
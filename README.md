# SmartConcierge – Hotel Chatbot

An AI chatbot that automatically answers hotel guest queries using Google's
Gemini API, grounded in your hotel's own data (rooms, amenities, policies, FAQs).

## Project Structure

```
smartconcierge/
├── app.py                    # Entry point — run this to chat
├── chatbot.py                # Gemini API integration & response logic
├── data_loader.py            # Loads and formats hotel_chatbot_data.json
├── prompt.py                 # Builds the system + user prompt
├── hotel_chatbot_data.json   # Hotel knowledge base (edit this for your property)
├── requirements.txt
├── .env.example               # Copy to .env and add your key
└── README.md
```

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_real_key_here
   ```

3. Run the chatbot:
   ```
   python app.py
   ```

## Customizing for a different hotel/restaurant

Just edit `hotel_chatbot_data.json` — update the name, rooms, amenities,
policies, and FAQs. No code changes needed; `data_loader.py` automatically
formats whatever is in that file into context for the model.

## How it works

1. `data_loader.py` reads `hotel_chatbot_data.json` and turns it into a
   plain-text context block.
2. `prompt.py` wraps that context plus the guest's question (and recent
   conversation history) into a prompt with clear instructions for the model.
3. `chatbot.py` sends that prompt to Gemini and returns the reply.
4. `app.py` runs the terminal chat loop, keeping track of conversation history.

## Notes

- If you see "Sorry, I couldn't find an answer for that question," it means
  the model determined the info isn't in your `hotel_chatbot_data.json` —
  just add the relevant details there.
- Rotate your API key immediately if it's ever been exposed (e.g. screenshotted,
  committed to git, or shared in chat/support tickets).
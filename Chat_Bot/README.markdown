# ChatBot

## Purpose
A simple interactive chatbot that responds to user input based on string similarity matching. Uses a JSON file to load an extensible set of response patterns for greetings, queries, and time requests.

## Features
- Matches user input to patterns in a `responses.json` file using string similarity.
- Supports dynamic time queries (e.g., "what time is it?").
- Handles case-insensitive input with a similarity threshold for relevant responses.
- Includes exit commands ("bye", "quit", "exit") to end the conversation.
- Robust error handling for invalid or empty inputs and JSON file issues.
- Displays similarity scores for transparency.

## Tech
- Python
- Standard library: `difflib`, `datetime`, `typing`, `json`, `os`

## How to Use
1. Ensure `responses.json` is in the `chatbot` directory with valid response patterns.
2. Navigate to the `chatbot` directory:
   ```bash
   cd chatbot
   ```
3. Run the script:
   ```bash
   python main.py
   ```
4. Interact with the chatbot:
   - Enter phrases like "hello", "how are you?", or "what time is it?" to get responses.
   - Type "bye", "quit", or "exit" to end the session.
5. View responses with similarity scores indicating match confidence.

## Directory
- `chatbot`

## Dependencies
- None (uses Python standard library)

## Troubleshooting
- **No Response or "Sorry, I didn't understand you"**: Ensure input is similar to patterns in `responses.json` (e.g., "hello", "what time is it?"). The similarity threshold requires a close match.
- **Empty Input**: Enter non-empty text when prompted.
- **File Not Found Error**: Ensure `responses.json` exists in the `chatbot` directory.
- **Invalid JSON Format**: Verify `responses.json` contains valid JSON (key-value pairs of strings).
- **Python Not Found**: Ensure Python 3.7+ is installed (`python --version`) and added to PATH.
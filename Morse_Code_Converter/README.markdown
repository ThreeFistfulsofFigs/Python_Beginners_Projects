# Morse Code Converter

## Purpose
Converts text to Morse code and vice versa, supporting letters, numbers, and common symbols. Provides an interactive command-line interface for easy use.

## Features
- Converts text to Morse code with space-separated codes.
- Converts Morse code back to text, handling single spaces (between letters) and double spaces (between words).
- Supports uppercase/lowercase letters, numbers (0-9), and symbols (e.g., ., ,, ?, !, @, &, etc.).
- Robust error handling for invalid inputs and Morse code characters.
- User-friendly menu with continue/exit options.

## Tech
- Python
- Standard library: `typing`

## How to Use
1. Navigate to the `morse_code_converter` directory:
   ```bash
   cd morse_code_converter
   ```
2. Run the script:
   ```bash
   python main.py
   ```
3. Choose an option:
   - **1**: Enter text (e.g., "Hello World!") to convert to Morse code.
   - **2**: Enter Morse code (e.g., ".... . .-.. .-.. ---  .-- --- .-. .-.. -..") to convert to text.
   - **3**: Exit the program.
4. Follow prompts to input text or Morse code and view results.
5. Choose to continue (y) or exit (n).

## Directory
- `morse_code_converter`

## Dependencies
- None (uses Python standard library)

## Troubleshooting
- **Invalid Input Errors**: Ensure text contains only supported characters (letters, numbers, listed symbols). For Morse code, use dots (.), dashes (-), single spaces between letters, and double spaces between words.
- **Empty Input**: Enter non-empty text or Morse code when prompted.
- **Python Not Found**: Ensure Python 3.7+ is installed (`python --version`) and added to PATH.
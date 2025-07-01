# ============================================================================
# MORSE CODE CONVERTER TOOL
# ============================================================================
# A comprehensive tool for converting text to Morse code and vice versa.
# Supports letters, numbers, common symbols, and includes interactive user
# interface with robust error handling for reliable conversions.
# ============================================================================

# Import required libraries
from typing import Dict  # For type annotations

# ============================================================================
# CONFIGURATION CONSTANTS
# ============================================================================
# Morse code dictionary including letters, numbers, and common symbols
MORSE_CODE_DICT: Dict[str, str] = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..',
    '!': '-.-.--', ' ': ' ', '/': '-..-.', '@': '.--.-.', '&': '.-...',
    '(': '-.--.', ')': '-.--.-', ':': '---...', ';': '-.-.-.', '=': '-...-',
    '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-',
    "'": '.----.', '*': '-..-'
}

# Reverse dictionary for Morse to text conversion
MORSE_TO_TEXT_DICT: Dict[str, str] = {value: key for key, value in MORSE_CODE_DICT.items()}

# Display formatting constants
SEPARATOR_LINE: str = "-" * 60
SECTION_HEADER: str = "=" * 70
SUCCESS_INDICATOR: str = "✓"
ERROR_INDICATOR: str = "✗"


# ============================================================================
# TEXT TO MORSE CONVERSION
# ============================================================================
def convert_to_morse(text: str) -> str:
    """
    Converts text to Morse code using the predefined dictionary.

    Args:
        text (str): The input text string to convert.

    Returns:
        str: The Morse code representation with spaces between codes.

    Raises:
        ValueError: If input text is empty or invalid.
        AttributeError: If input is not a valid string.
    """
    try:
        # INPUT VALIDATION
        if not text:
            raise ValueError("Input text cannot be empty")

        # TEXT CONVERSION
        # Convert each character to its Morse code equivalent
        return " ".join(MORSE_CODE_DICT.get(char.upper(), '') for char in text)

    except AttributeError:
        raise ValueError("Invalid input: Please provide a valid string")


# ============================================================================
# MORSE TO TEXT CONVERSION
# ============================================================================
def convert_to_text(morse: str) -> str:
    """
    Converts Morse code back to text using the reverse dictionary.

    Args:
        morse (str): The Morse code string to convert (space-separated codes).

    Returns:
        str: The decoded text string.

    Raises:
        ValueError: If input Morse code is empty or contains invalid characters.
        AttributeError: If input is not a valid string.
    """
    try:
        # INPUT VALIDATION
        if not morse:
            raise ValueError("Input Morse code cannot be empty")

        # MORSE CODE PARSING
        # Split on double spaces for words, single spaces for characters
        words = morse.strip().split('  ')
        result = []

        # WORD-BY-WORD CONVERSION
        for word in words:
            chars = word.split()
            converted = ''.join(MORSE_TO_TEXT_DICT.get(char, '') for char in chars)
            result.append(converted)

        return ' '.join(result)

    except KeyError as e:
        raise ValueError(f"Invalid Morse code character: {e}")
    except AttributeError:
        raise ValueError("Invalid input: Please provide a valid Morse code string")


# ============================================================================
# INTERACTIVE MODE FUNCTIONALITY
# ============================================================================
def main() -> None:
    """
    Main function to provide interactive Morse code conversion interface.

    Handles user input, performs conversions, and displays results with
    comprehensive error handling.
    """
    print(f"{SECTION_HEADER}")
    print("MORSE CODE CONVERTER")
    print(f"{SECTION_HEADER}")

    while True:
        try:
            # MENU DISPLAY
            print("\nOptions:")
            print("1. Convert text to Morse code")
            print("2. Convert Morse code to text")
            print("3. Exit")

            # USER INPUT COLLECTION
            choice = input("Enter your choice (1-3): ").strip()

            # TEXT TO MORSE CONVERSION
            if choice == '1':
                user_input = input("Enter text to convert to Morse code: ")
                result = convert_to_morse(user_input)
                print(f"{SEPARATOR_LINE}")
                print(f"Morse code: {result}")
                print(f"{SEPARATOR_LINE}")

            # MORSE TO TEXT CONVERSION
            elif choice == '2':
                print("Enter Morse code (use space between letters, double space between words)")
                morse_input = input("Example: .... . .-.. .-.. ---  .-- --- .-. .-.. -..: ")
                result = convert_to_text(morse_input)
                print(f"{SEPARATOR_LINE}")
                print(f"Text: {result}")
                print(f"{SEPARATOR_LINE}")

            # EXIT CONDITION
            elif choice == '3':
                print(f"{SUCCESS_INDICATOR} Exiting Morse Code Converter")
                break

            else:
                print(f"{ERROR_INDICATOR} Invalid choice. Please enter 1, 2, or 3.")

        # ERROR HANDLING
        except ValueError as ve:
            print(f"{ERROR_INDICATOR} Error: {ve}")
        except Exception as e:
            print(f"{ERROR_INDICATOR} Unexpected error: {e}")

        # CONTINUE PROMPT
        continue_choice = input("\nDo you want to continue? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print(f"{SUCCESS_INDICATOR} Exiting Morse Code Converter")
            break


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    main()

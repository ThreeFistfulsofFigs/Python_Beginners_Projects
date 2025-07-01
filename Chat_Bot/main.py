# ============================================================================
# CHATBOT TOOL
# ============================================================================
# A simple interactive chatbot that responds to user input based on string
# similarity matching. Supports predefined responses loaded from a JSON file
# and dynamic time queries with robust error handling and user-friendly interaction.
# ============================================================================

# Import required libraries
from difflib import SequenceMatcher  # For string similarity comparison
from datetime import datetime  # For handling time queries
from typing import Dict, Tuple  # For type annotations
import json  # For loading responses from JSON file
import os  # For checking file existence

# ============================================================================
# CONFIGURATION CONSTANTS
# ============================================================================
# Display formatting constants
SEPARATOR_LINE: str = "-" * 60
SECTION_HEADER: str = "=" * 70
SUCCESS_INDICATOR: str = "✓"
ERROR_INDICATOR: str = "✗"

# Similarity threshold for response matching
SIMILARITY_THRESHOLD: float = 0.6  # Minimum similarity for valid response

# JSON file for responses
RESPONSES_FILE: str = "responses.json"

# ============================================================================
# CHATBOT CLASS
# ============================================================================
class ChatBot:
    """
    A chatbot that responds to user input based on string similarity matching.

    Attributes:
        name (str): The name of the chatbot.
        responses (Dict[str, str]): Dictionary mapping input patterns to responses.
    """
    def __init__(self, name: str, responses: Dict[str, str]) -> None:
        """
        Initializes the chatbot with a name and response dictionary.

        Args:
            name (str): The name of the chatbot.
            responses (Dict[str, str]): Dictionary of input patterns and responses.
        """
        self.name = name
        self.responses = responses

    @staticmethod
    def calculate_similarity(input_sentence: str, response_sentence: str) -> float:
        """
        Calculates the similarity ratio between two strings using SequenceMatcher.

        Args:
            input_sentence (str): The user's input string.
            response_sentence (str): The response pattern to compare against.

        Returns:
            float: The similarity ratio between 0.0 and 1.0.

        Raises:
            AttributeError: If inputs are not valid strings.
        """
        try:
            # STRING SIMILARITY CALCULATION
            sequence: SequenceMatcher = SequenceMatcher(a=input_sentence.lower(), b=response_sentence.lower())
            return sequence.ratio()
        except AttributeError:
            raise AttributeError("Invalid input: Both arguments must be strings")

    def gets_best_response(self, user_input: str) -> Tuple[str, float]:
        """
        Finds the best response based on input similarity to response patterns.

        Args:
            user_input (str): The user's input string.

        Returns:
            Tuple[str, float]: The best response and its similarity score.

        Raises:
            ValueError: If input is empty or invalid.
        """
        try:
            # INPUT VALIDATION
            if not user_input.strip():
                raise ValueError("Input cannot be empty")

            # RESPONSE MATCHING
            highest_similarity: float = 0.0
            best_match: str = "Sorry, I didn't understand you."

            for response_key in self.responses:
                similarity: float = ChatBot.calculate_similarity(user_input, response_key)
                if similarity > highest_similarity and similarity >= SIMILARITY_THRESHOLD:
                    highest_similarity = similarity
                    best_match = self.responses[response_key]

            return best_match, highest_similarity

        except AttributeError:
            raise ValueError("Invalid input: Please provide a valid string")

    def run(self) -> None:
        """
        Runs the interactive chatbot interface.

        Handles user input, displays responses, and manages the conversation loop
        with comprehensive error handling.
        """
        print(f"{SECTION_HEADER}")
        print(f"WELCOME TO {self.name.upper()} CHATBOT")
        print(f"{SECTION_HEADER}")
        print(f"Hello! My name is {self.name}, how can I help you?")

        while True:
            try:
                # USER INPUT COLLECTION
                user_input: str = input("You: ").strip()

                # EXIT CONDITION
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"{SEPARATOR_LINE}")
                    print(f"{SUCCESS_INDICATOR} Goodbye! Have a nice day!")
                    print(f"{SEPARATOR_LINE}")
                    break

                # RESPONSE PROCESSING
                response, similarity = self.gets_best_response(user_input)

                # SPECIAL RESPONSE HANDLING
                if response == "GET_TIME":
                    response = f"The time is {datetime.now():%H:%M}"

                # RESPONSE DISPLAY
                print(f"{SEPARATOR_LINE}")
                print(f"{self.name}: {response} (Similarity: {similarity:.2f})")
                print(f"{SEPARATOR_LINE}")

            # ERROR HANDLING
            except ValueError as ve:
                print(f"{ERROR_INDICATOR} Error: {ve}")
            except Exception as e:
                print(f"{ERROR_INDICATOR} Unexpected error: {e}")

# ============================================================================
# RESPONSE LOADING
# ============================================================================
def load_responses(file_path: str) -> Dict[str, str]:
    """
    Loads response patterns from a JSON file.

    Args:
        file_path (str): Path to the JSON file containing responses.

    Returns:
        Dict[str, str]: Dictionary of response patterns and their responses.

    Raises:
        FileNotFoundError: If the JSON file does not exist.
        json.JSONDecodeError: If the JSON file is invalid.
    """
    try:
        # FILE EXISTENCE CHECK
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Response file '{file_path}' not found")

        # JSON LOADING
        with open(file_path, 'r', encoding='utf-8') as file:
            responses: Dict[str, str] = json.load(file)
        return responses

    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Invalid JSON format in '{file_path}'")
    except Exception as e:
        raise Exception(f"Error loading responses: {e}")

# ============================================================================
# MAIN PROGRAM LOGIC
# ============================================================================
def main() -> None:
    """
    Main function to initialize and run the chatbot.

    Loads responses from a JSON file and starts the chatbot in interactive mode.
    """
    try:
        # RESPONSE LOADING
        responses: Dict[str, str] = load_responses(RESPONSES_FILE)

        # CHATBOT INITIALIZATION
        chatbot: ChatBot = ChatBot(name="ChatBob", responses=responses)
        chatbot.run()

    # COMPREHENSIVE ERROR HANDLING
    except FileNotFoundError as e:
        print(f"{ERROR_INDICATOR} {e}")
    except json.JSONDecodeError as e:
        print(f"{ERROR_INDICATOR} {e}")
    except KeyboardInterrupt:
        print(f"\n{ERROR_INDICATOR} Chatbot interrupted by user")
    except Exception as e:
        print(f"{ERROR_INDICATOR} Unexpected error during chatbot execution: {e}")

# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    main()
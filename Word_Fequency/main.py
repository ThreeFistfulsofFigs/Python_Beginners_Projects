# ============================================================================
# WORD FREQUENCY ANALYZER
# ============================================================================
# This script analyzes text to count word frequencies. It supports both
# manual text input and file-based analysis with a user-friendly interface.
# ============================================================================

# Import required libraries
from collections import Counter  # For efficient counting of words
import re  # For regular expression pattern matching
import os  # For operating system interface (environment variables)
import tkinter as tk  # For GUI components
from tkinter import filedialog  # For file selection dialog


# ============================================================================
# CORE ANALYSIS FUNCTION
# ============================================================================
def get_frequency(text: str, limit: int = None) -> list[tuple[str, int]]:
    """
    Analyzes the input text and returns a list of tuples containing words and their frequencies.

    Args:
        text (str): The input text to analyze.
        limit (int, optional): The maximum number of most common words to return. If None, returns all.

    Returns:
        list[tuple[str, int]]: A list of (word, frequency) tuples, sorted by frequency in descending order,
                              limited by the specified number if provided.
    """
    # TEXT PREPROCESSING
    # Convert all text to lowercase to ensure case-insensitive counting
    # This means "The" and "the" will be counted as the same word
    lowered_text = text.lower()

    # WORD EXTRACTION
    # Use regex to find all words in the text
    # \b = word boundary (start/end of word)
    # \w+ = one or more word characters (letters, digits, underscore)
    # This pattern excludes punctuation and whitespace
    words: list[str] = re.findall(r'\b\w+\b', lowered_text)

    # FREQUENCY COUNTING
    # Counter automatically counts occurrences of each word
    # It creates a dictionary-like object with word:count pairs
    words_counts: Counter[str] = Counter(words)

    # RESULT FORMATTING
    # Convert Counter to list of tuples, sorted by frequency (highest first)
    # Apply limit if specified by user
    if limit is not None:
        return list(words_counts.most_common(limit))
    return list(words_counts.most_common())


# ============================================================================
# FILE READING FUNCTION
# ============================================================================
def read_text_from_file(file_path: str) -> str:
    """
    Reads and returns the content of a text file.

    Args:
        file_path (str): The path to the .txt file to read.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: If there is an error reading the file.
    """
    try:
        # FILE READING WITH PROPER ENCODING
        # Use UTF-8 encoding to handle international characters
        # 'with' statement ensures file is properly closed even if error occurs
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read entire file content and remove leading/trailing whitespace
            return file.read().strip()

    # ERROR HANDLING
    # Handle case where file doesn't exist
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} was not found.")

    # Handle other file reading errors (permissions, corruption, etc.)
    except IOError as e:
        raise IOError(f"Error reading the file: {e}")


# ============================================================================
# GUI-BASED FILE SELECTION WITH FALLBACK
# ============================================================================
def get_file_path() -> str:
    """
    Prompts the user to select a .txt file using a GUI dialog if possible, otherwise falls back to manual entry.

    Returns:
        str: The path to the selected file.
    """
    # GUI AVAILABILITY TEST
    # Test if tkinter GUI is available and working before attempting file dialog
    # This prevents freezing on systems where GUI doesn't work properly
    try:
        test_root = tk.Tk()  # Create test window
        test_root.withdraw()  # Hide the test window
        test_root.update()  # Force processing of GUI events
        test_root.destroy()  # Clean up test window
        gui_available = True
    except Exception:
        gui_available = False

    # ENVIRONMENT CHECK
    # Check if running in headless environment (no display server)
    # DISPLAY environment variable exists on Unix/Linux systems with GUI
    # Windows (os.name == 'nt') typically has GUI available
    if not gui_available or os.environ.get('DISPLAY') is None and os.name != 'nt':
        print("GUI not available. Using manual file path entry.")
        return get_manual_file_path()

    # GUI FILE DIALOG ATTEMPT
    try:
        # TKINTER SETUP
        root = tk.Tk()  # Create main window
        root.withdraw()  # Hide main window (we only want dialog)
        root.attributes('-topmost', True)  # Bring dialog to front of other windows
        root.update()  # Process any pending GUI events

        # DIALOG TIMING
        # Add small delay to let GUI system settle
        root.after(100, lambda: None)

        # FILE DIALOG
        # Show file selection dialog with appropriate filters
        file_path = filedialog.askopenfilename(
            parent=root,  # Set parent window for proper dialog behavior
            title="Select a text file",  # Dialog title
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]  # File type filters
        )

        # CLEANUP
        root.destroy()  # Clean up the root window

        # HANDLE USER CANCELLATION
        if not file_path:
            print("No file selected. Using manual entry.")
            return get_manual_file_path()

        return file_path

    # FALLBACK ON GUI FAILURE
    except Exception as e:
        print(f"GUI file selection failed: {e}")
        return get_manual_file_path()


# ============================================================================
# MANUAL FILE PATH ENTRY WITH VALIDATION
# ============================================================================
def get_manual_file_path() -> str:
    """
    Helper function for manual file path entry with validation.

    Returns:
        str: The path to the selected file.
    """
    print("Please enter the path to your text file.")

    # INPUT LOOP
    # Continue asking for input until valid file path is provided
    while True:
        file_path = input("File path: ").strip()

        # PATH CLEANUP
        # Remove quotes that users often add when copying file paths
        # Handle both single and double quotes
        if (file_path.startswith('"') and file_path.endswith('"')) or \
                (file_path.startswith("'") and file_path.endswith("'")):
            file_path = file_path[1:-1]

        # EMPTY PATH CHECK
        if not file_path:
            print("Please enter a valid file path.")
            continue

        # FILE VALIDATION
        try:
            # Attempt to open and read from file to verify it exists and is readable
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read(1)  # Read just one character to test file access
            return file_path

        # SPECIFIC ERROR HANDLING
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            print("Please check the path and try again.")
        except PermissionError:
            print(f"Permission denied: {file_path}")
        except Exception as e:
            print(f"Error reading file: {e}")
            print("Please try again.")


# ============================================================================
# MAIN PROGRAM LOGIC
# ============================================================================
def main() -> None:
    """
    Main function to handle user input, file selection, and display word frequencies.
    """
    # USER INPUT SOURCE SELECTION
    # Ask user whether they want to type text manually or analyze a file
    while True:
        source_choice = input("Enter text manually (m) or analyze a .txt file (f)? ").lower().strip()
        if source_choice in ['m', 'f']:
            break
        print("Please enter 'm' for manual input or 'f' for file analysis.")

    # TEXT INPUT HANDLING
    if source_choice == 'm':
        # MANUAL TEXT INPUT
        # Get text directly from user input and clean whitespace
        text: str = input("Enter your text: ").strip()
    else:
        # FILE-BASED INPUT
        # Get file path using GUI or manual entry
        file_path = get_file_path()
        try:
            # Read text content from selected file
            text = read_text_from_file(file_path)
        except (FileNotFoundError, IOError) as e:
            # Handle file reading errors and exit gracefully
            print(f"Error: {e}. Exiting.")
            return

    # LIMIT SPECIFICATION
    # Ask user how many top words they want to see (optional)
    while True:
        limit_input = input("Enter the number of most common words to display (press Enter for all): ")

        # NO LIMIT CASE
        if not limit_input.strip():
            limit = None
            break

        # NUMERIC LIMIT VALIDATION
        try:
            limit = int(limit_input)
            if limit <= 0:
                raise ValueError("Limit must be a positive number.")
            break
        except ValueError as e:
            print(f"Please enter a valid positive number. {str(e)}")

    # FREQUENCY ANALYSIS
    # Calculate word frequencies using the core analysis function
    word_frequencies: list[tuple[str, int]] = get_frequency(text, limit)

    # RESULTS DISPLAY
    # Show results to user in a clean format
    if not word_frequencies:
        print("No words found in the text.")
    else:
        # Display each word with its frequency count
        print("\nWord Frequency Results:")
        print("-" * 30)
        for word, frequency in word_frequencies:
            print(f"{word}: {frequency}")


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    # Execute main function only when script is run directly
    # (not when imported as a module)
    main()
from collections import Counter
import re


def get_frequency(text: str) -> list[tuple[str, int]]:
    """
    Analyzes the input text and returns a list of tuples containing words and their frequencies.

    Args:
        text (str): The input text to analyze.

    Returns:
        list[tuple[str, int]]: A list of (word, frequency) tuples, sorted by frequency in descending order.
    """
    # Convert text to lowercase for case-insensitive counting
    lowered_text = text.lower()
    # Extract all words using regex (matches word characters bounded by word boundaries)
    words: list[str] = re.findall(r'\b\w+\b', lowered_text)
    # Count the frequency of each word using Counter
    words_counts: Counter[str] = Counter(words)
    # Return the most common words as a list of tuples
    return list(words_counts.most_common())


def main() -> None:
    """
    Main function to handle user input and display word frequencies.
    """
    # Get input text from the user and remove leading/trailing whitespace
    text: str = input("Enter your text: ").strip()
    # Calculate word frequencies
    word_frequencies: list[tuple[str, int]] = get_frequency(text)

    # Display each word and its frequency
    for word, frequency in word_frequencies:
        print(f"{word}: {frequency}")


if __name__ == "__main__":
    # Executes the main function when the script is run directly
    main()
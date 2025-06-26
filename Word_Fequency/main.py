from collections import Counter
import re


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
    # Convert text to lowercase for case-insensitive counting
    lowered_text = text.lower()
    # Extract all words using regex (matches word characters bounded by word boundaries)
    words: list[str] = re.findall(r'\b\w+\b', lowered_text)
    # Count the frequency of each word using Counter
    words_counts: Counter[str] = Counter(words)
    # Return the most common words, limited by the specified number if provided
    if limit is not None:
        return list(words_counts.most_common(limit))
    return list(words_counts.most_common())


def main() -> None:
    """
    Main function to handle user input and display word frequencies.
    """
    # Get input text from the user and remove leading/trailing whitespace
    text: str = input("Enter your text: ").strip()

    # Get the limit for the number of most common words (optional)
    while True:
        limit_input = input("Enter the number of most common words to display (press Enter for all): ")
        if not limit_input.strip():
            limit = None
            break
        try:
            limit = int(limit_input)
            if limit <= 0:
                raise ValueError("Limit must be a positive number.")
            break
        except ValueError as e:
            print(f"Please enter a valid positive number. {str(e)}")

    # Calculate word frequencies
    word_frequencies: list[tuple[str, int]] = get_frequency(text, limit)

    # Display each word and its frequency
    if not word_frequencies:
        print("No words found in the text.")
    else:
        for word, frequency in word_frequencies:
            print(f"{word}: {frequency}")


if __name__ == "__main__":
    # Executes the main function when the script is run directly
    main()
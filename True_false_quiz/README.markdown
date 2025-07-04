# Quiz Game

## Purpose
This project implements a console-based true/false quiz game that presents a series of questions to the user, tracks their score, and displays the final results. It is designed to demonstrate object-oriented programming, data management, and user interaction in Python, making it suitable for beginners learning to structure multi-file Python applications.

## Features
- Presents a series of true/false questions from a predefined dataset.
- Tracks the user's score and displays it after each question.
- Provides immediate feedback on correct/incorrect answers.
- Supports case-insensitive answer validation (True/False).
- Displays a final score summary upon quiz completion.
- Modular design with separate classes for question data and quiz logic.

## Tech
- **Python**: Core language for logic and user interaction.
- **Standard Library**: Uses `input` for user interaction and basic data handling.
- **Modules**: None beyond the standard library.

## How to Use
1. Navigate to the `quiz_game` directory:
   ```bash
   cd quiz_game
   ```
2. Ensure Python 3.7 or higher is installed:
   ```bash
   python --version
   ```
3. Run the main script:
   ```bash
   python main.py
   ```
4. Follow the prompts to answer each question with `True` or `False`.
5. After answering all questions, view your final score in the format `correct_answers/total_questions`.
6. To exit, wait for the quiz to complete or interrupt with `Ctrl+C`.

## Dependencies
- None (uses only Python standard library).

## Troubleshooting
- **Invalid Input**: Enter only `True` or `False` (case-insensitive) when prompted. Other inputs may not be validated and could affect scoring.
- **No Questions Displayed**: Ensure `data.py` exists in the `quiz_game` directory and contains valid question data.
- **Python Not Found**: Verify Python 3.7+ is installed and added to PATH (`python --version`). Use the full path (e.g., `/usr/bin/python3`) if needed.
- **File Not Found Error**: Confirm all required files (`main.py`, `question_model.py`, `quiz_brain.py`, `data.py`) are in the `quiz_game` directory.
- **Unexpected Termination**: If the program stops unexpectedly, check for syntax errors in `data.py` or ensure the question data format includes `question` and `correct_answer` keys.

## Notes
- The question dataset in `data.py` includes additional metadata (e.g., category, difficulty) for potential future enhancements, such as question filtering or multiple-choice support.
- The program can be extended by adding more questions to `data.py` or implementing features like question randomization or category selection.
- To create a standalone executable, use PyInstaller:
  ```bash
  pip install pyinstaller
  pyinstaller --onefile main.py
  ```

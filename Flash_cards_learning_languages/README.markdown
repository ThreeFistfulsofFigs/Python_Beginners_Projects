# Flashcard Language Learning App

## Overview
The Flashcard Language Learning App is a GUI-based application designed to help users learn vocabulary through interactive flashcards. It supports user-uploaded CSV files for custom language pairs (e.g., Slovenian-English, French-English) with three learning modes, spaced repetition, and progress tracking. Users can switch between saved language pairs with their associated CSV data and progress, configured via a dedicated settings window.

## Features
- **Three Learning Modes**:
  - **Learn New Words**: Displays words from the selected CSV, excluding those marked as familiar or unfamiliar.
  - **Repeat Unfamiliar Words**: Reviews words marked as needing practice (via the "wrong" button).
  - **Repeat Familiar Words**: Reviews words marked as learned (via the "right" button).
- **Spaced Repetition**: Cycles through words in order for lists of 50 or fewer words; uses random selection with no recent repeats (last 5 words) for larger lists.
- **Progress Tracking**: Saves unfamiliar and familiar words to language-specific JSON files (e.g., `slovenian-english_words_to_learn.json`).
- **Encouragement Message**: Displays a motivational message every 20 new words learned, suggesting a switch to "Repeat Familiar Words" mode.
- **Display Order Toggle**: Choose whether the front or back language (e.g., Slovenian or English) is shown first.
- **Automatic Card Flip**: Flips to the back (opposite language) after 5 seconds.
- **Button Actions**:
  - **Right Button**: Marks a word as learned (adds to `words_learned`, removes from `words_to_learn`).
  - **Wrong Button**: Marks a word as unfamiliar (adds to `words_to_learn`, removes from `words_learned` in familiar mode).
- **Custom Language Support**:
  - Upload a two-column CSV file and specify custom language names via a settings window.
  - Persist language configurations (CSV path, language names) in `data/language_configs.json`.
  - Switch between saved language pairs (e.g., Slovenian-English, French-English) via a dropdown, restoring the associated CSV and progress.
- **Modern GUI**: Uses `ttkbootstrap` with a superhero theme for a clean, responsive interface.

## Technologies
- **Python**: Core programming language.
- **ttkbootstrap**: For modern GUI styling (superhero theme).
- **Pillow**: For loading and processing card images (`card_front.png`, `card_back.png`).
- **pandas**: For reading CSV vocabulary files.
- **json**: For saving/loading progress and language configurations to/from JSON files.
- **tkinter**: For the GUI framework, including `filedialog` for CSV uploads and `Toplevel` for settings.
- **Standard Libraries**: `os`, `random`, `collections` (for `deque`), `tkinter.messagebox`.

## Setup
1. **Prerequisites**:
   - Python 3.7 or higher, installed and added to PATH.
     ```bash
     python --version
     ```
   - Ensure `tkinter` is installed (included with Python, but on Linux, install with):
     ```bash
     sudo apt-get install python3-tk
     ```

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/ThreeFistfulsofFigs/Python_Beginners_Projects.git
   cd Python_Beginners_Projects/flashcard_app
   ```

3. **Set Up Virtual Environment** (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

4. **Install Dependencies**:
   ```bash
   pip install ttkbootstrap pandas Pillow
   ```

5. **Prepare Data and Assets**:
   - Place a default `slovenian_words.csv` in the `data` folder (e.g., `./data/slovenian_words.csv`) for initial use.
     - Format: CSV with two columns (e.g., `Slovenian,English\npes,dog\n...`).
   - Place `card_front.png` and `card_back.png` in the `images` folder (e.g., `./images/`).
   - Ensure write permissions for the `data` folder to save language-specific JSON files and `language_configs.json`.

## Usage
1. Navigate to the project folder:
   ```bash
   cd flashcard_app
   ```
2. Run the application:
   ```bash
   python main.py
   ```
3. **Interact with the GUI**:
   - **Load New Language**:
     - Click "Settings" to open the settings window.
     - Enter names for the front and back languages (e.g., "French" and "English").
     - Click "Load CSV" and select a two-column CSV file (e.g., `french_words.csv`).
     - The new language pair (e.g., French-English) is added to the language dropdown, and its configuration is saved.
   - **Switch Languages**:
     - Use the "Language" dropdown to switch between saved language pairs (e.g., Slovenian-English, French-English).
     - The app loads the associated CSV and progress files automatically.
   - **Settings**:
     - **Display Order**: Select the front or back language to choose which appears first.
     - **Mode**:
       - **Learn New Words**: Shows new words from the selected CSV, excluding familiar/unfamiliar words.
       - **Repeat Unfamiliar Words**: Reviews words marked as unfamiliar (shows message if empty).
       - **Repeat Familiar Words**: Reviews words marked as learned (shows message if empty).
   - **Flashcards**:
     - View the front of the card (e.g., Slovenian or French word).
     - Wait 5 seconds for an automatic flip to the back (e.g., English translation), or click "right" or "wrong" to flip immediately.
     - On the back:
       - Click **Right**: Marks the word as learned, adds to `words_learned`, removes from `words_to_learn`.
       - Click **Wrong**: Marks the word as unfamiliar, adds to `words_to_learn`, removes from `words_learned` (in familiar mode).
   - **Progress**:
     - Every 20 new words learned, a message encourages switching to "Repeat Familiar Words".
     - Progress is saved to `data/<language-pair>_words_to_learn.json` and `data/<language-pair>_words_learned.json`.
4. **Reset Progress**:
   - Delete the language-specific JSON files (e.g., `data/french-english_words_to_learn.json`) to reset progress for that language.
   - Re-uploading a CSV for an existing language pair overwrites its data and resets progress.

## Troubleshooting
- **GUI Not Displaying**:
  - Ensure `tkinter` is installed (`sudo apt-get install python3-tk` on Linux).
  - Verify Python is configured for graphical applications (e.g., a display server on Linux).
- **File Not Found: CSV**:
  - Ensure the CSV file exists at the path stored in `language_configs.json` (defaults to `data/slovenian_words.csv`).
  - Check file path and permissions.
- **Invalid CSV Format**:
  - Ensure the CSV has exactly two columns (e.g., `French,English`).
  - Verify UTF-8 encoding and valid data.
- **File Not Found: `card_front.png` or `card_back.png`**:
  - Ensure images are in the `images` folder.
  - Verify file names and paths.
- **JSON File Errors**:
  - Check write permissions for the `data` folder.
  - If JSON files are corrupted, delete the language-specific JSON files or `language_configs.json` to reset.
- **No Words Displayed**:
  - Ensure the loaded CSV contains valid data.
  - In "Repeat Unfamiliar Words" or "Repeat Familiar Words", add words by marking them as unfamiliar (wrong) or learned (right) in "Learn New Words" mode.
- **Module Not Found**:
  - Install dependencies: `pip install ttkbootstrap pandas Pillow`.
  - Verify the virtual environment is activated.
- **Styling Issues**:
  - Ensure `ttkbootstrap` is installed (`pip install ttkbootstrap>=1.10.1`).
  - Try a different theme by modifying `themename` in `main.py` (e.g., "darkly", "cyborg").

## Notes
- The loaded CSV is never modified; progress is stored in language-specific JSON files.
- Language configurations (CSV paths, language names) are persisted in `data/language_configs.json`.
- Progress is reset when a new CSV is uploaded for an existing language pair.
- Future enhancements planned:
  - Support for JSON data loading as an alternative to CSV.
  - Additional GUI enhancements for usability.
  - Dedicated reset function to clear progress without deleting files manually.
- Can be converted to an executable using PyInstaller (e.g., `pyinstaller --onefile main.py`).
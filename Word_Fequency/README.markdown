# Word Frequency Analyzer

## Overview
The Word Frequency Analyzer is a Python tool that counts word frequencies in text, supporting both manual input and `.txt` file analysis. It uses a Tkinter GUI for file selection (with manual fallback) and provides a sorted list of word frequencies, ideal for text analysis or linguistic studies.

## Features
- **Text Analysis**: Counts word frequencies in manual input or `.txt` files.
- **GUI File Selection**: Uses Tkinter for easy file selection (falls back to manual entry).
- **Limit Option**: Restricts output to top N words (optional).
- **Case Insensitive**: Treats words like "The" and "the" as identical.
- **Error Handling**: Manages file access and input errors gracefully.

## Requirements
- **Operating System**: Any (Windows, macOS, Linux)
- **Python**: 3.7 or higher
- **Dependencies**: Built-in `collections`, `re`, `os`, `tkinter`

## Installation

### Step 1: Set Up Environment
1. **Install Python**: Ensure Python 3.7+ is installed and added to PATH.
   ```bash
   python --version
   ```
2. **Create Virtual Environment** (optional but recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

### Step 2: Run the Script
1. **Locate Script**: Navigate to the project directory containing `main.py`.
2. **Run the Script**:
   ```bash
   python main.py
   ```

## Usage

### Step 1: Analyze Text
1. **Choose Input Method**:
   - Enter `m` for manual text input or `f` for file analysis.
2. **Manual Input**:
   - Type text and press Enter.
3. **File Input**:
   - Select `.txt` file via GUI dialog or enter path manually.
4. **Set Limit**:
   - Enter number of top words to display (e.g., `10`) or press Enter for all.
5. **View Results**:
   - Output shows word frequencies (e.g., `the: 25`, `and: 15`).

### Step 2: Testing
1. **Test Manual Input**:
   - Input text (e.g., `The quick brown fox`) and verify frequencies.
2. **Test File Input**:
   - Select a `.txt` file and confirm correct word counts.
3. **Test Error Handling**:
   - Enter non-existent file path to verify error message.
   - Input invalid limit (e.g., `-1`) to confirm retry prompt.

## Troubleshooting

### "File not found"
- Ensure file path is correct and accessible.
- Verify `.txt` file format for file input.

### Tkinter GUI Issues
- Ensure `tkinter` is installed: `sudo apt-get install python3-tk` (Linux).
- If GUI fails, script falls back to manual path entry.

## Files Included
- `main.py`: Core script with text analysis and GUI logic.

## Notes
- **Version**: 1.0.0
- **Encoding**: Uses UTF-8 for file operations to support international characters.

## Support
For issues, check console output or submit an issue at [GitHub repository URL] (replace with your repo URL).
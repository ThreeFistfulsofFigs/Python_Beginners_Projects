# Magic Notepad

## Overview
Magic Notepad is a simple Python-based text editor with a Tkinter GUI, offering basic file operations like saving and loading text files. It provides a clean, user-friendly interface for note-taking or editing text files.

## Features
- **Text Editing**: Edit text in a scrollable, word-wrapping text area.
- **File Operations**: Save and load `.txt` files via GUI dialogs.
- **Error Handling**: Manages file access errors gracefully.
- **Minimalist Design**: Simple interface with save/load buttons.

## Requirements
- **Operating System**: Any (Windows, macOS, Linux)
- **Python**: 3.7 or higher
- **Dependencies**: Built-in `tkinter` module

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

### Step 2: Run the Application
1. **Locate Script**: Navigate to the project directory containing `main.py`.
2. **Run the Script**:
   ```bash
   python main.py
   ```

## Usage

### Step 1: Use the Notepad
1. **Edit Text**: Type or paste text into the text area.
2. **Save File**: Click "Save" to choose a location and save as `.txt`.
3. **Load File**: Click "Load" to select and open a `.txt` file.
4. **Verify Operations**:
   - Console confirms save/load actions (e.g., `File saved to: notes.txt`).
   - Text area updates with loaded content.

### Step 2: Testing
1. **Test Save**:
   - Enter text, save to a file, and verify file contents.
2. **Test Load**:
   - Load a `.txt` file and confirm text appears in the text area.
3. **Test Error Handling**:
   - Attempt to load a non-existent file to verify error message.

## Troubleshooting

### "Error saving/loading file"
- Ensure file path is accessible and has write/read permissions.
- Verify `.txt` file format for loading.

### Tkinter GUI Issues
- Ensure `tkinter` is installed (included with standard Python).
- On Linux, install Tkinter: `sudo apt-get install python3-tk`.

## Files Included
- `main.py`: Core script with GUI and file operation logic.

## Notes
- **Version**: 1.0.0
- **Encoding**: Uses UTF-8 for file operations to support international characters.

## Support
For issues, check console output or submit an issue at [GitHub repository URL] (replace with your repo URL).
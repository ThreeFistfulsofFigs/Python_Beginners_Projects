# Pomodoro Timer

## Overview
The Pomodoro Timer is a GUI-based application built with Python's `tkinter` library, implementing the Pomodoro Technique to enhance productivity through timed work and break sessions. It features customizable timers, multiple themes, a progress ring, motivational quotes, session tracking, and data persistence via JSON.

## Features
- **Customizable Timers**: Set work, short break, and long break durations (default: 25/5/30 minutes).
- **Multiple Themes**: Choose from default, dark, forest, and ocean themes with distinct color schemes.
- **Progress Ring**: Visualizes session progress with a dynamic ring and color changes based on urgency.
- **Motivational Quotes**: Displays random quotes after work sessions to encourage users.
- **Session Tracking**: Tracks daily session count and total focused time, with a checkmark system for completed sessions.
- **Data Persistence**: Saves settings and session stats to `pomodoro_settings.json`.
- **Keyboard Shortcuts**: Space (start/pause/resume), R (reset), S (settings), T (toggle theme).
- **Sound Notifications**: Plays beeps for session transitions (Windows only; system bell elsewhere).
- **Responsive GUI**: Clean interface with a tomato icon or emoji fallback, stats display, and settings window.

## Tech
- **Python**: Core programming language.
- **tkinter**: For the graphical user interface.
- **winsound**: For notification sounds on Windows.
- **json**, **os**, **datetime**, **random**, **platform**, **threading**: Standard library modules for data handling, file operations, and platform-specific features.

## How to Use
1. Ensure Python 3.7+ is installed (`python --version`).
2. Navigate to the `pomodoro_timer` directory:
   ```bash
   cd pomodoro_timer
   ```
3. Run the application:
   ```bash
   python main.py
   ```
4. **Interact with the GUI**:
   - Click "Start" or press Space to begin a session (toggles to Pause/Resume).
   - Click "Reset" or press R to reset the timer.
   - Click "Settings" or press S to adjust timer durations and themes.
   - Click "Theme" or press T to cycle through themes.
   - View session stats and checkmarks at the bottom.
5. Close the window to save settings and exit.

## Dependencies
- **tkinter**: Included in Python's standard library. On Linux, install with:
  ```bash
  sudo apt-get install python3-tk
  ```
- **winsound**: Included in Python's standard library (Windows only).
- No additional packages required.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/ThreeFistfulsofFigs/Python_Beginners_Projects.git
   cd Python_Beginners_Projects/pomodoro_timer
   ```
2. Run `main.py`:
   ```bash
   python main.py
   ```

## Notes
- **Optional File**: Place a `tomato.png` (200x224 pixels) in the project directory for a custom tomato icon; otherwise, a red oval with a tomato emoji is used.
- **Data Storage**: Settings and stats are saved to `pomodoro_settings.json` in the project directory.
- **Executable**: Convert to a standalone executable using PyInstaller:
  ```bash
  pip install pyinstaller
  pyinstaller --onefile --windowed main.py
  ```

## Troubleshooting
- **GUI Not Displaying**: Ensure `tkinter` is installed (`sudo apt-get install python3-tk` on Linux).
- **Sound Issues**: On non-Windows systems, sounds fall back to the system bell (`\a`). Ensure system audio is enabled.
- **File Errors**: Check write permissions for `pomodoro_settings.json` if saving fails.
- **Window Not Responding**: Ensure the window is focused for keyboard shortcuts to work.

## License
MIT (see repository's LICENSE file).
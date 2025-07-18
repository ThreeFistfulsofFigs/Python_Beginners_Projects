# Pomodoro Timer (Kivy Version)

## Overview
The Pomodoro Timer (Kivy Version) is a GUI-based application built with Python's `kivy` library, implementing the Pomodoro Technique to enhance productivity through timed work and break sessions. This is an alternative implementation of the Tkinter-based Pomodoro Timer, offering a modern UI with similar functionality, including customizable timers, light/dark themes, session tracking, and motivational quotes.

## Features
- **Customizable Timers**: Set work, short break, and long break durations (default: 25/5/30 minutes).
- **Light/Dark Themes**: Toggle between light and dark themes with dynamic color updates.
- **Session Statistics**: Tracks daily session count, focused time, and streak.
- **Session History**: Displays a scrollable log of the last 10 sessions with timestamps.
- **Motivational Quotes**: Shows random quotes after work sessions for encouragement.
- **Keyboard Shortcuts**: Space (start/pause), R (reset), S (settings), T (toggle theme).
- **Sound Notifications**: Plays beeps for session transitions (Windows only; system bell elsewhere).
- **Data Persistence**: Saves settings and session history to `pomodoro_settings.json`.
- **Responsive GUI**: Modern interface with a tomato image (or placeholder text if missing), stats display, and settings popup.

## Tech
- **Python**: Core programming language.
- **kivy**: For the modern graphical user interface.
- **winsound**: For notification sounds on Windows.
- **json**, **os**, **datetime**, **random**, **platform**, **threading**: Standard library modules for data handling, file operations, and platform-specific features.

## How to Use
1. Ensure Python 3.7+ is installed (`python --version`).
2. Install Kivy:
   ```bash
   pip install kivy
   ```
3. Navigate to the `pomodoro_timer_kivy` directory:
   ```bash
   cd pomodoro_timer_kivy
   ```
4. Run the application:
   ```bash
   python main.py
   ```
5. **Interact with the GUI**:
   - Click "START" or press Space to begin/pause a session.
   - Click "RESET" or press R to reset the timer.
   - Click "SETTINGS" or press S to adjust timer durations.
   - Click "THEME" or press T to toggle between light and dark themes.
   - View session stats and history on the right panel.
6. Close the window to save settings and exit.

## Dependencies
- **kivy**: Install with:
  ```bash
  pip install kivy
  ```
- **winsound**: Included in Python's standard library (Windows only).
- No additional packages required for standard library modules.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/ThreeFistfulsofFigs/Python_Beginners_Projects.git
   cd Python_Beginners_Projects/pomodoro_timer_kivy
   ```
2. Install dependencies:
   ```bash
   pip install kivy
   ```
3. Run `main.py`:
   ```bash
   python main.py
   ```

## Notes
- **Optional File**: Place a `tomato.png` (recommended 175x175 pixels) in the project directory for the timer image; otherwise, a "[Tomato Image Missing]" placeholder is displayed.
- **Data Storage**: Settings and session history are saved to `pomodoro_settings.json` in the project directory.
- **Executable**: Convert to a standalone executable using PyInstaller:
  ```bash
  pip install pyinstaller
  pyinstaller --onefile --windowed main.py
  ```
- **Comparison with Tkinter Version**: This Kivy version offers a more modern, cross-platform UI compared to the Tkinter version, but lacks the additional themes (forest, ocean) and progress ring animation. It uses a simpler layout with a focus on session history and stats.

## Troubleshooting
- **GUI Not Displaying**: Ensure `kivy` is installed correctly (`pip install kivy`) and Python is configured for graphical applications (e.g., ensure a display server is running on Linux).
- **Sound Issues**: On non-Windows systems, sounds fall back to the system bell (`\a`). Ensure system audio is enabled.
- **File Errors**: Check write permissions for `pomodoro_settings.json` if saving fails.
- **Window Not Responding**: Ensure the window is focused for keyboard shortcuts to work.
- **Kivy Installation Issues**: Verify dependencies (SDL2, GLEW, etc.) are installed. On Linux, you may need:
  ```bash
  sudo apt-get install python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
  ```

## License
MIT (see repository's LICENSE file).
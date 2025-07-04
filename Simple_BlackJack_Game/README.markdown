# Blackjack Game

## Overview
This project implements a console-based Blackjack game where a user plays against a computer dealer. The game follows standard Blackjack rules, using a deck with aces valued at 1 or 11 and face cards at 10. It provides an interactive experience with a clear console interface, a logo display, and logic for handling blackjacks, busts, and winner determination.

## Features
- **Interactive Gameplay**: Users can choose to hit or stand, with immediate feedback on hand scores.
- **Blackjack Detection**: Automatically detects blackjacks (Ace + 10-value card) for both user and computer.
- **Dynamic Scoring**: Adjusts ace values (11 to 1) to prevent busting when possible.
- **Console Interface**: Clears the console between games and displays a logo using the `art` library.
- **Computer AI**: Computer dealer follows standard rules, hitting until the score is at least 17.

## Tech
- **Python**: Core programming language.
- **Modules**: `random`, `os`, `art`.

## How to Use
1. Navigate to the `blackjack` directory:
   ```bash
   cd blackjack
   ```
2. Ensure dependencies are installed (see [Dependencies](#dependencies)).
3. Run the game:
   ```bash
   python main.py
   ```
4. Follow prompts:
   - Type `y` to start a new game or `n` to exit.
   - During gameplay, type `y` to hit (draw another card) or `n` to stand.
5. View results after each round, including hands, scores, and winner.

## Directory
- **blackjack**: Contains `main.py` and this `README.md`.

## Dependencies
- **art>=5.9**: For displaying the game logo.
  ```bash
  pip install art
  ```

## Setup
1. Ensure Python 3.7 or higher is installed:
   ```bash
   python --version
   ```
2. Install the `art` library:
   ```bash
   pip install art
   ```
3. Run `main.py` as described in [How to Use](#how-to-use).

## Troubleshooting
- **Module Not Found**:
  - Ensure the `art` library is installed (`pip install art`).
  - Verify the virtual environment is activated if used.
- **Console Not Clearing**:
  - Ensure `os` module is supported on your platform (Windows, macOS, or Linux).
  - On Windows, use `cls`; on Unix-based systems, use `clear`.
- **Invalid Input**:
  - Enter `y` or `n` when prompted for gameplay decisions.
  - Inputs are case-insensitive, but other characters may cause unexpected behavior.

## Notes
- **Game Rules**: Follows standard Blackjack rules (e.g., dealer hits on 16 or less, stands on 17 or more).
- **Executable**: Can be converted to a standalone executable using PyInstaller (e.g., `pyinstaller --onefile main.py`).
- **Error Handling**: The game gracefully handles invalid inputs by prompting again.
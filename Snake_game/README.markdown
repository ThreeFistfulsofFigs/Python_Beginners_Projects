# Snake Game

## Overview
This project implements a classic Snake game using Python's Turtle graphics module. The player controls a snake that grows by consuming food, with the goal of achieving the highest score without colliding with the walls or the snake's own tail. The game features a clean interface, smooth controls, and a scoreboard, making it an engaging way to learn object-oriented programming and event-driven game development.

## Features
- **Interactive Gameplay**: Control the snake using arrow keys to navigate and collect food.
- **Dynamic Growth**: The snake extends when it consumes food, increasing the score.
- **Collision Detection**: Game ends on collision with walls or the snake's tail, displaying a "GAME OVER" message.
- **Score Tracking**: Real-time score display updated with each food consumed.
- **Responsive Graphics**: Smooth animations using Turtle graphics with a black background and white snake segments.
- **Modular Design**: Separate classes for Snake, Food, and Scoreboard for maintainable code.

## Tech
- **Python**: Core programming language.
- **turtle**: For rendering graphics and handling user input.
- **random**: For generating random food positions.
- **time**: For controlling game speed via frame delays.

## How to Use
1. Ensure Python 3.7 or higher is installed and added to your PATH.
2. Navigate to the `snake_game` directory:
   ```bash
   cd snake_game
   ```
3. Run the game:
   ```bash
   python main.py
   ```
4. Use the arrow keys (Up, Down, Left, Right) to control the snake.
5. Collect blue food circles to grow the snake and increase your score.
6. Avoid hitting the walls or the snake's tail, which ends the game.
7. Click the window to exit after the "GAME OVER" message appears.

## Directory
- `snake_game`
  - `main.py`: Main game loop and logic.
  - `snake.py`: Snake class for movement and growth.
  - `food.py`: Food class for random placement.
  - `scoreboard.py`: Scoreboard class for score display and game-over message.

## Dependencies
- **turtle**: Included in Python's standard library. Requires `tkinter` for graphical rendering.
  - On Linux, install `tkinter` if needed:
    ```bash
    sudo apt-get install python3-tk
    ```

## Troubleshooting
- **Window Not Displaying**:
  - Ensure `tkinter` is installed (`sudo apt-get install python3-tk` on Linux).
  - Verify Python is configured to display graphical windows (e.g., ensure a display server is running on Linux).
- **Slow Performance**:
  - The game uses a 0.1-second delay for smooth animation. If performance is slow, reduce the game speed by increasing the `time.sleep(0.1)` value in `main.py`.
- **No Response to Arrow Keys**:
  - Ensure the game window is in focus when pressing arrow keys.
  - Verify key bindings in `main.py` match your keyboard (e.g., `"Up"`, `"Down"`, `"Left"`, `"Right"`).
- **Module Not Found**:
  - Confirm Python 3.7+ is used: `python --version`.
  - Ensure all files (`main.py`, `snake.py`, `food.py`, `scoreboard.py`) are in the `snake_game` directory.

## Notes
- The game window is fixed at 600x600 pixels for consistent gameplay.
- The snake moves in a grid-like pattern (20-unit steps) for precise control.
- Can be converted to an executable using PyInstaller (e.g., `pyinstaller --onefile main.py`).

## License
MIT (see `LICENSE` file in the repository root).

## Contact
For questions or suggestions, open an issue on the [GitHub repository](https://github.com/ThreeFistfulsofFigs/Python_Beginners_Projects) or email [gerrit.meurer952@dontsp.am](mailto:gerrit.meurer952@dontsp.am).
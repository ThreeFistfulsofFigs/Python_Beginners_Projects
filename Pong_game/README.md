# Pong Game

## Overview
This project implements a classic Pong game using Python's Turtle graphics module. Two players control paddles to hit a ball back and forth across the screen, with the goal of scoring points by getting the ball past the opponent's paddle. The game features smooth paddle controls, realistic ball physics, and a scoreboard that tracks points for both players, making it an excellent introduction to game development and object-oriented programming concepts.

## Features
- **Two-Player Gameplay**: Left player uses W/S keys, right player uses Up/Down arrow keys for paddle control.
- **Realistic Ball Physics**: Ball bounces off walls and paddles with consistent movement patterns.
- **Collision Detection**: Accurate detection for wall bounces, paddle hits, and scoring zones.
- **Score Tracking**: Real-time score display for both players with large, visible numbers.
- **Smooth Controls**: Responsive paddle movement with 25-unit increments for precise control.
- **Visual Design**: Clean black background with white paddles and violet ball for clear visibility.
- **Modular Architecture**: Separate classes for Ball, Paddle, and Scoreboard for maintainable code.

## Tech
- **Python**: Core programming language.
- **turtle**: For rendering graphics and handling user input.
- **time**: For controlling game speed and frame rate.

## How to Use
1. Ensure Python 3.7 or higher is installed and added to your PATH.
2. Navigate to the `pong_game` directory:
   ```bash
   cd pong_game
   ```
3. Run the game:
   ```bash
   python main.py
   ```
4. **Player Controls**:
   - **Left Player**: Use 'W' key to move up, 'S' key to move down
   - **Right Player**: Use 'Up' arrow to move up, 'Down' arrow to move down
5. Hit the ball with your paddle to send it toward your opponent.
6. Score points by getting the ball past your opponent's paddle.
7. The game continues indefinitely - first to reach your target score wins!
8. Click the window to exit the game.

## Directory
- `pong_game`
  - `main.py`: Main game loop and collision detection logic.
  - `paddle.py`: Paddle class for player-controlled paddles.
  - `ball.py`: Ball class for movement and bouncing mechanics.
  - `scoreboard.py`: Scoreboard class for score display and tracking.

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
- **Sluggish Performance**:
  - The game uses a 0.06-second delay for smooth animation. If performance is slow, increase the `time.sleep(0.06)` value in `main.py`.
- **Paddles Not Responding**:
  - Ensure the game window is in focus when pressing keys.
  - Verify key bindings: Left player uses 'W'/'S', right player uses 'Up'/'Down' arrows.
- **Ball Moving Too Fast/Slow**:
  - Adjust the `x_movement` and `y_movement` values in `ball.py` (currently set to 10).
- **Module Not Found**:
  - Confirm Python 3.7+ is used: `python --version`.
  - Ensure all files (`main.py`, `paddle.py`, `ball.py`, `scoreboard.py`) are in the `pong_game` directory.

## Game Mechanics
- **Ball Movement**: The ball moves diagonally across the screen, bouncing off top and bottom walls.
- **Paddle Collision**: When the ball hits a paddle, it reverses horizontal direction.
- **Scoring**: Points are awarded when the ball passes beyond a paddle (left boundary = right player scores, right boundary = left player scores).
- **Ball Reset**: After each point, the ball returns to center and reverses direction for the next serve.
- **Boundary Detection**: Ball bounces off top/bottom walls but passes through left/right boundaries for scoring.

## Notes
- The game window is fixed at 800x600 pixels for optimal gameplay experience.
- Paddles move in 25-unit increments for smooth, controllable movement.
- Ball collision detection uses distance calculation for accurate paddle hits.
- The game runs continuously until manually closed - no win condition implemented.
- Can be converted to an executable using PyInstaller (e.g., `pyinstaller --onefile main.py`).

## License
MIT (see `LICENSE` file in the repository root).

## Contact
For questions or suggestions, open an issue on the [GitHub repository](https://github.com/ThreeFistfulsofFigs/Python_Beginners_Projects) or email [gerrit.meurer952@dontsp.am](mailto:gerrit.meurer952@dontsp.am).
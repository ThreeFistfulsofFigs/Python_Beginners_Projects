# Modern Art Painting Generator

## Overview
The Modern Art Painting Generator is a Python project that creates a visually appealing modern art piece using the Turtle graphics module. It draws a grid of colored dots with random colors from a predefined list and saves the artwork as a PNG image. This project is ideal for beginners to explore Python’s Turtle graphics and image processing.

## Purpose
The project generates a 10x10 grid of colored dots with random RGB colors, demonstrating Turtle graphics for drawing and PIL for saving graphical output as a PNG. It includes a commented-out reference for extracting colors from an image using the `colorgram` library.

## Features
- Draws a 10x10 grid of 100 dots, each 20 units in diameter, spaced 50 units apart.
- Uses a predefined list of RGB colors for vibrant, random dot coloring.
- Saves the artwork as a PNG file (`modern_art_drawing.png`) using a screenshot-based approach.
- Includes a commented-out reference for extracting colors from an image (`image.jpg`) using `colorgram`.
- Interactive exit by clicking the Turtle graphics window.
- Fast rendering with optimized Turtle speed settings.

## Tech
- **Python**: Core language for logic and graphics.
- **turtle**: Standard library module for drawing the dot grid.
- **random**: Standard library module for selecting random colors.
- **os**: Standard library module for file operations (e.g., removing temporary files).
- **PIL (Pillow)**: For capturing and saving the Turtle canvas as a PNG.

## How to Use
1. Ensure Python 3.7+ is installed and added to PATH:
   ```bash
   python --version
   ```
2. Install the required dependency:
   ```bash
   pip install Pillow
   ```
3. Navigate to the project directory:
   ```bash
   cd modern_art_painting_generator
   ```
4. Run the script:
   ```bash
   python main.py
   ```
5. Watch the Turtle draw a 10x10 grid of colored dots.
6. Click the Turtle window to exit.
7. Check the project directory for the output file `modern_art_drawing.png`.

## Dependencies
- **Pillow**: `Pillow>=8.0.0` (for image processing and saving).
- **turtle**: Requires `tkinter`. On Linux, install with:
  ```bash
  sudo apt-get install python3-tk
  ```

## Troubleshooting
- **GUI Issues**: Ensure `tkinter` is installed (`sudo apt-get install python3-tk` on Linux).
- **Window Not Displaying**: Verify Python is configured to display graphical windows (e.g., ensure a display server is running on Linux).
- **Module Not Found**:
  - Install Pillow: `pip install Pillow`.
  - Verify the correct Python environment is used: `python -m pip install Pillow`.
- **File Not Saved**: Ensure write permissions in the project directory and check for `temp.eps` cleanup issues.
- **Commented-Out Color Extraction Code**: To use the `colorgram` reference, install `colorgram.py` (`pip install colorgram.py`) and provide a valid `image.jpg` in the project directory.

## Notes
- The commented-out color extraction code requires `colorgram.py` and a valid image file (`image.jpg`) to extract RGB colors dynamically.
- The project can be converted to an executable using PyInstaller (e.g., `pyinstaller --onefile main.py`).
- Output file (`modern_art_drawing.png`) is saved in the project directory.
# Colorful Spirograph

## Overview
This project creates a visually appealing spirograph pattern using Python's `turtle` graphics module. The turtle draws a series of circles with a fixed radius, rotating slightly after each circle and changing colors randomly to produce a vibrant, layered spirograph design. This project is ideal for beginners learning about Python’s turtle graphics, random number generation, and graphical programming.

## Features
- **Dynamic Color Patterns**: Generates random RGB colors for each circle using the `random` module, creating a visually engaging effect.
- **Spirograph Design**: Draws 100 circles with a 5-degree rotation between each, forming a spirograph-like pattern.
- **Interactive Exit**: Closes the turtle graphics window when the user clicks, providing an intuitive way to end the program.
- **Fast Rendering**: Uses the fastest turtle speed to quickly generate the pattern.
- **Customizable Turtle**: Configures the turtle with a circle shape for a polished appearance.

## Tech Stack
- **Python**: Core programming language.
- **turtle**: Standard library module for graphics and drawing.
- **random**: Standard library module for generating random RGB colors.

## Dependencies
- None (uses Python standard library: `turtle`, `random`).

## How to Use
1. Ensure Python 3.7 or higher is installed:
   ```bash
   python --version
   ```
2. Navigate to the project directory:
   ```bash
   cd colorful_spirograph
   ```
3. Run the script:
   ```bash
   python main.py
   ```
4. Watch the turtle draw a colorful spirograph pattern.
5. Click the graphics window to exit.

## Setup
1. **Clone the Repository** (if not already done):
   ```bash
   git clone https://github.com/ThreeFistfulsofFigs/Python_Beginners_Projects.git
   cd Python_Beginners_Projects/colorful_spirograph
   ```
2. No additional dependencies are required, as the project uses only the Python standard library.
3. Ensure `tkinter` is installed for turtle graphics:
   - On Linux, install `tkinter` if needed:
     ```bash
     sudo apt-get install python3-tk
     ```
   - On Windows and macOS, `tkinter` is typically included with Python.

## Troubleshooting
- **Window Not Displaying**:
  - Ensure `tkinter` is installed (`sudo apt-get install python3-tk` on Linux).
  - Verify a display server is running (e.g., X11 or Wayland on Linux).
- **Slow Performance**:
  - The turtle speed is set to `"fastest"`. If performance is still slow, reduce the number of iterations (e.g., change `range(100)` to `range(50)` in `main.py`).
- **No Colors Displayed**:
  - Ensure `screen.colormode(255)` is set correctly to enable RGB colors.
- **Unexpected Termination**:
  - Check for syntax errors or ensure Python 3.7+ is used.

## Notes
- **Executable**: The project can be converted to a standalone executable using PyInstaller:
  ```bash
  pip install pyinstaller
  pyinstaller --onefile main.py
  ```
  The executable will be in the `dist` folder.
- **Customization**: Modify the circle radius (default: 120), rotation angle (default: 5 degrees), or number of iterations (default: 100) in `main.py` to experiment with different patterns.
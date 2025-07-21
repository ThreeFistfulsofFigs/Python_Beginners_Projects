# Python Beginners Projects

## Overview
This repository contains a collection of small, standalone Python projects designed for beginners to explore practical programming concepts. Each project solves everyday problems or demonstrates specific Python techniques, making it ideal for learning and experimentation. Projects include tools for currency conversion, expense splitting, financial planning, text editing, password generation, website monitoring, text analysis, word frequency analysis, VPN kill switch configuration, Morse code conversion, a simple chatbot, a Markdown to PDF converter, a Blackjack game, a true/false quiz game, a random turtle walk visualization, a colorful spirograph generator, a modern art painting generator, a classic Snake game, a classic Pong game, a Pomodoro timer (with Tkinter and Kivy versions), and a miles to kilometers converter.

## Projects

### 1. Currency Converter
- **Purpose**: Converts amounts between currencies using real-time exchange rates from the freecurrencyapi.com API, with a fallback to a local JSON file (`rates.json`) for offline use.
- **Features**:
  - Fetches live rates via API or uses cached rates.
  - Robust input validation with retry logic.
  - Saves API rates to `rates.json` for offline access.
- **Tech**: Python, `requests`, `json`, `typing`.
- **How to Use**: Run `main.py` with a valid API key, enter amount and currencies, and view results.
- **Directory**: `currency_converter`
- **Dependencies**: `requests>=2.25.0`

### 2. EPUB to PDF Converter
- **Purpose**: Converts EPUB files to PDF format using a Tkinter GUI, preserving pagination and handling images/links.
- **Features**:
  - GUI for selecting EPUB files and output directory.
  - Processes EPUB content with optimized PDF styling.
  - Detailed logging and progress feedback.
- **Tech**: Python, `tkinter`, `ebooklib`, `beautifulsoup4`, `pdfkit`, `wkhtmltopdf`.
- **How to Use**: Run `main.py`, select an EPUB file and output directory, and click "Convert to PDF".
- **Directory**: `epub_to_pdf_converter`
- **Dependencies**: `ebooklib>=0.17.1`, `beautifulsoup4>=4.9.0`, `pdfkit>=0.7.0`, `wkhtmltopdf`

### 3. Expense Splitting Calculator
- **Purpose**: Splits expenses among multiple people based on custom percentage contributions.
- **Features**:
  - Validates percentages to sum to 100%.
  - Formats output with locale-based currency (e.g., €1,234.56).
  - Handles invalid inputs with retry prompts.
- **Tech**: Python, `locale`.
- **How to Use**: Run `main.py`, enter total amount and number of people, then input percentages.
- **Directory**: `expense_splitting_calculator`
- **Dependencies**: None (standard library)

### 4. Personal Finance Calculator
- **Purpose**: Calculates taxes, net income, and available funds after expenses with monthly/yearly breakdowns.
- **Features**:
  - Detailed financial summary with locale-based currency formatting.
  - Input validation for reliable calculations.
- **Tech**: Python, `locale`.
- **How to Use**: Run `main.py`, input monthly income, tax rate, and expenses, and view results.
- **Directory**: `personal_finance_calculator`
- **Dependencies**: None (standard library)

### 5. Magic Notepad
- **Purpose**: A simple text editor with a Tkinter GUI for editing, saving, and loading text files.
- **Features**:
  - Scrollable text area with word wrapping.
  - Save/load `.txt` files via GUI dialogs.
  - UTF-8 support for international characters.
- **Tech**: Python, `tkinter`.
- **How to Use**: Run `main.py`, edit text, and use "Save" or "Load" buttons.
- **Directory**: `magic_notepad`
- **Dependencies**: None (standard library)

### 6. Password Generator
- **Purpose**: Generates cryptographically secure passwords with customizable length and character types.
- **Features**:
  - Uses `secrets` module for secure random generation.
  - Evaluates password strength based on complexity.
  - Validates required character types (e.g., uppercase, symbols).
- **Tech**: Python, `secrets`, `string`, `re`.
- **How to Use**: Run `main.py` to generate 10 passwords with strength scores.
- **Directory**: `password_generator`
- **Dependencies**: None (standard library)

### 7. Website Status Checker
- **Purpose**: Monitors website availability and performance, analyzing HTTP responses and security headers.
- **Features**:
  - Reports status codes, response times, and server details.
  - Checks security headers (e.g., HSTS, CSP).
  - Supports single URL and batch processing.
- **Tech**: Python, `requests`, `urllib.parse`.
- **How to Use**: Run `main.py` for a sample URL check or enable interactive mode for manual URL input.
- **Directory**: `website_status_checker`
- **Dependencies**: `requests>=2.25.0`

### 8. Word Frequency Analyzer
- **Purpose**: Analyzes word frequencies in text, supporting manual input or `.txt` file analysis.
- **Features**:
  - GUI file selection with manual fallback.
  - Case-insensitive word counting with optional limit.
  - Handles file errors gracefully.
- **Tech**: Python, `collections`, `re`, `os`, `tkinter`.
- **How to Use**: Run `main.py`, choose manual or file input, and view word frequencies.
- **Directory**: `word_frequency_analyzer`
- **Dependencies**: None (standard library)

### 9. Text Analyzer
- **Purpose**: Analyzes text files for detailed statistics, including character, word, sentence, and paragraph counts, as well as word frequency distributions, using an enhanced Tkinter GUI.
- **Features**:
  - GUI for file selection, text preview, and results display.
  - Comprehensive text analysis with word frequency.
  - Supports multiple file encodings (UTF-8, Latin-1, CP1252, ISO-8859-1).
  - Text preview toggle (500-character preview or full text).
  - Saves analysis results to `.txt` files.
  - Responsive GUI with minimum window size of 800x600.
- **Tech**: Python, `tkinter`, `collections`, `re`, `os`, `pathlib`, `typing`.
- **How to Use**: Run `main.py`, select a `.txt` or `.md` file, click "Analyze" to view statistics, use "Show Full Text"/"Show Preview Only" to toggle preview, view detailed results, or save to a file.
- **Directory**: `text_analyzer`
- **Dependencies**: None (standard library)

### 10. VPN Kill Switch Configuration Tool
- **Purpose**: Configures a Windows kill switch to disable internet access when a VPN is inactive, ensuring secure network usage.
- **Features**:
  - GUI for configuring VPN processes, network interface, and monitoring intervals.
  - Real-time monitoring of service, VPN, and network status.
  - Automatically disables network if no VPN processes are detected.
  - Logs events to `%USERPROFILE%\vpn_killswitch.log`.
- **Tech**: Python, `tkinter`, `psutil`, `pywin32`.
- **How to Use**: Run `main.py`, configure VPN processes (e.g., `surfshark.exe`) and network interface, start the kill switch service, and monitor status.
- **Directory**: `vpn_killswitch`
- **Dependencies**: `psutil>=5.8.0`, `pywin32>=306`

### 14. Blackjack Game
- **Purpose**: A console-based Blackjack game where users play against a computer dealer following standard Blackjack rules.
- **Features**:
  - Interactive gameplay with hit/stand choices.
  - Automatic blackjack detection for user and computer.
  - Dynamic ace scoring (11 or 1) to prevent busting.
  - Console clearing and graphic display (using a local `art.py` file) for an enhanced interface.
  - Computer dealer hits until score is at least 17.
- **Tech**: Python, `random`, `os`, `art` (local `art.py` file).
- **How to Use**: Ensure `art.py` is in the `blackjack` directory, run `main.py`, type `y` to start or `n` to exit, and choose `y` to hit or `n` to stand during gameplay.
- **Directory**: `blackjack`
- **Dependencies**: None (requires local `art.py` file in the project directory)

### 15. Quiz Game
- **Purpose**: A console-based true/false quiz game that presents questions, tracks scores, and displays results, designed to teach object-oriented programming and data management.
- **Features**:
  - Presents true/false questions from a predefined dataset.
  - Tracks and displays user score after each question.
  - Provides immediate feedback on correct/incorrect answers.
  - Supports case-insensitive answer validation.
  - Displays final score summary upon completion.
  - Modular design with separate question and quiz logic classes.
- **Tech**: Python, standard library (`input`, basic data handling).
- **How to Use**: Run `main.py`, answer questions with `True` or `False`, and view final score. Exit with `Ctrl+C` if needed.
- **Directory**: `quiz_game`
- **Dependencies**: None (standard library)

### 16. Random Turtle Walk
- **Purpose**: Creates a visually engaging random walk pattern using Python's turtle graphics module, with random directions and RGB pen colors.
- **Features**:
  - Generates a random walk with 500 steps, each 50 units long.
  - Uses random RGB colors for the turtle's pen to create vibrant patterns.
  - Moves in four cardinal directions (0°, 90°, 180°, 270°) for a grid-like effect.
  - Thick pen size (10) for clear visibility of the pattern.
  - High turtle speed for quick rendering of the design.
  - Closes the window when the user clicks, providing an interactive exit.
- **Tech**: Python, `turtle`, `random`.
- **How to Use**: Run `main.py`, watch the turtle draw a random pattern with changing colors, and click the window to exit.
- **Directory**: `random_turtle_walk`
- **Dependencies**: None (standard library)

### 17. Colorful Spirograph
- **Purpose**: Creates a vibrant spirograph pattern using Python’s turtle graphics, with random RGB colors and a layered circular design.
- **Features**:
  - Draws 100 circles with a fixed radius and 5-degree rotation between each.
  - Uses random RGB colors for each circle to create a colorful effect.
  - Fast rendering with the turtle’s fastest speed setting.
  - Interactive exit by clicking the graphics window.
- **Tech**: Python, `turtle`, `random`.
- **How to Use**: Run `main.py`, watch the turtle draw a colorful spirograph pattern, and click the window to exit.
- **Directory**: `colorful_spirograph`
- **Dependencies**: None (standard library)

### 18. Modern Art Painting Generator
- **Purpose**: Creates a modern art piece using Python’s turtle graphics, drawing a 10x10 grid of colored dots with random RGB colors, saved as a PNG image.
- **Features**:
  - Draws a 10x10 grid of 100 dots, each 20 units in diameter, spaced 50 units apart.
  - Uses a predefined list of RGB colors for vibrant, random dot coloring.
  - Saves the artwork as a PNG file (`modern_art_drawing.png`) using a screenshot-based approach.
  - Includes a commented-out reference for extracting colors from an image using `colorgram`.
  - Interactive exit by clicking the Turtle graphics window.
- **Tech**: Python, `turtle`, `random`, `os`, `Pillow`.
- **How to Use**: Run `main.py`, watch the turtle draw the dot grid, and click the window to exit. The output is saved as `modern_art_drawing.png`.
- **Directory**: `modern_art_painting_generator`
- **Dependencies**: `Pillow>=8.0.0`

### 19. Snake Game
- **Purpose**: A classic Snake game where players control a snake to collect food, grow, and avoid collisions with walls or its own tail, using Python’s Turtle graphics.
- **Features**:
  - Interactive gameplay with arrow key controls.
  - Dynamic snake growth and score increase on food consumption.
  - Collision detection for walls and tail, with a "GAME OVER" message.
  - Real-time score display using a scoreboard.
  - Smooth animations with a modular design for snake, food, and scoreboard.
- **Tech**: Python, `turtle`, `random`, `time`.
- **How to Use**: Run `main.py`, use arrow keys to control the snake, collect food to grow, and avoid collisions. Click the window to exit after "GAME OVER".
- **Directory**: `snake_game`
- **Dependencies**: None (standard library, requires `tkinter` for `turtle`)

### 20. Pong Game
- **Purpose**: A classic Pong game where two players control paddles to hit a ball back and forth, scoring points when the opponent misses, using Python’s Turtle graphics.
- **Features**:
  - Two-player gameplay: Left player uses W/S keys, right player uses Up/Down arrow keys.
  - Realistic ball physics with consistent bouncing patterns.
  - Accurate collision detection for walls, paddles, and scoring zones.
  - Real-time score display with large, visible numbers.
  - Smooth paddle controls with 25-unit movement increments.
  - Clean visual design with a black background, white paddles, and a violet ball.
  - Modular architecture with separate classes for Ball, Paddle, and Scoreboard.
- **Tech**: Python, `turtle`, `time`.
- **How to Use**: Run `main.py`, use W/S keys for the left paddle and Up/Down arrows for the right paddle, score points by getting the ball past the opponent, and click the window to exit.
- **Directory**: `pong_game`
- **Dependencies**: None (standard library, requires `tkinter` for `turtle`)

### 21. Miles to Kilometers Converter
- **Purpose**: A simple GUI application that converts miles to kilometers using Python's tkinter library, featuring an intuitive interface with real-time conversion capabilities.
- **Features**:
  - Clean, organized layout with clearly labeled input and output fields.
  - Multiple input methods: Click "Calculate" button or press Enter key.
  - Precise conversion using the international standard factor (1 mile = 1.609344 kilometers).
  - Error handling for invalid inputs with graceful fallback to zero display.
  - Grid-based layout matching standard converter applications.
  - Comprehensive banner-style code documentation.
- **Tech**: Python, `tkinter`.
- **How to Use**: Run `main.py`, enter a number in the input field, and either click "Calculate" or press Enter to see the result in kilometers.
- **Directory**: `miles_to_km_converter`
- **Dependencies**: None (standard library, requires `tkinter`)

### 22. Pomodoro Timer (Tkinter Version)
- **Purpose**: A GUI-based Pomodoro Timer implementing the Pomodoro Technique to enhance productivity through timed work and break sessions, built with Tkinter.
- **Features**:
  - Customizable work, short break, and long break durations (default: 25/5/30 minutes).
  - Multiple themes: default, dark, forest, and ocean.
  - Progress ring visualizing session progress with dynamic color changes.
  - Random motivational quotes displayed after work sessions.
  - Session tracking with daily stats and checkmarks for completed sessions.
  - Data persistence via `pomodoro_settings.json`.
  - Keyboard shortcuts: Space (start/pause/resume), R (reset), S (settings), T (toggle theme).
  - Sound notifications for session transitions (Windows only; system bell elsewhere).
- **Tech**: Python, `tkinter`, `winsound` (Windows only), `json`, `os`, `datetime`, `random`, `platform`, `threading`.
- **How to Use**: Run `main.py`, click "Start" or press Space to begin, use buttons or shortcuts to control, and adjust settings/themes as needed.
- **Directory**: `pomodoro_timer`
- **Dependencies**: None (standard library, requires `tkinter`)

### 23. Pomodoro Timer (Kivy Version)
- **Purpose**: A GUI-based Pomodoro Timer implementing the Pomodoro Technique, built with Kivy as an alternative to the Tkinter version, offering a modern UI with similar functionality.
- **Features**:
  - Customizable work, short break, and long break durations (default: 25/5/30 minutes).
  - Light and dark themes with dynamic color updates.
  - Session statistics tracking daily sessions, focused time, and streak.
  - Scrollable session history for the last 10 sessions.
  - Random motivational quotes displayed after work sessions.
  - Keyboard shortcuts: Space (start/pause), R (reset), S (settings), T (toggle theme).
  - Sound notifications for session transitions (Windows only; system bell elsewhere).
  - Data persistence via `pomodoro_settings.json`.
- **Tech**: Python, `kivy`, `winsound` (Windows only), `json`, `os`, `datetime`, `random`, `platform`, `threading`.
- **How to Use**: Run `main.py`, click "START" or press Space to begin/pause, use buttons or shortcuts to control, and adjust settings/themes as needed.
- **Directory**: `pomodoro_timer_kivy`
- **Dependencies**: `kivy>=2.0.0`

### 24. Password Manager Pro
- **Purpose**: A secure password management application with a modern Tkinter GUI, featuring AES-256 encryption for storing and managing passwords.
- **Features**:
  - Secure storage with AES-256 encryption using Fernet and PBKDF2 key derivation.
  - Master password authentication with up to 3 attempts, verified by decrypting a test string.
  - Add, view, edit, delete, and search passwords with a tabbed interface.
  - Generate strong passwords with customizable length and character types.
  - Import/export passwords as JSON (exported passwords are decrypted).
  - Theme switching (superhero, darkly, cyborg, vapor) and context menus for usability.
  - Local storage in `passwords.json` and `config.json`.
- **Tech**: Python, `tkinter`, `ttkbootstrap`, `cryptography`, `json`, `os`, `datetime`, `secrets`, `base64`.
- **How to Use**: Run `main.py`, set a master password on first run or enter it on subsequent runs, use the GUI to add/view/edit/delete passwords, generate new passwords, or import/export data.
- **Directory**: `password_manager`
- **Dependencies**: `ttkbootstrap>=1.10.1`, `cryptography>=36.0.0`

## Getting Started

### Prerequisites
- **Python**: 3.7 or higher, installed and added to PATH.
  ```bash
  python --version
  ```
- **External Tool** (for EPUB to PDF Converter and Markdown to PDF Converter): `wkhtmltopdf` (see project-specific README).
- **Dependencies**:
  - Currency Converter: `requests>=2.25.0`
  - EPUB to PDF Converter: `ebooklib>=0.17.1`, `beautifulsoup4>=4.9.0`, `pdfkit>=0.7.0`, `wkhtmltopdf`
  - Markdown to PDF Converter: `markdown2>=2.3.0`, `pdfkit>=0.7.0`, `wkhtmltopdf`
  - Word Frequency Analyzer: None (standard library)
  - Text Analyzer: None (standard library)
  - VPN Kill Switch Configuration Tool: `psutil>=5.8.0`, `pywin32>=306`
  - Morse Code Converter: None (standard library)
  - ChatBot: None (standard library)
  - Blackjack Game: None (requires local `art.py` file in the project directory)
  - Quiz Game: None (standard library)
  - Random Turtle Walk: The turtle module requires `tkinter`. Install on Linux with `sudo apt-get install python3-tk`.
  - Colorful Spirograph: None (standard library)
  - Modern Art Painting Generator: `Pillow>=8.0.0`
  - Snake Game: None (standard library, requires `tkinter` for `turtle`)
  - Pong Game: None (standard library, requires `tkinter` for `turtle`)
  - Pomodoro Timer (Tkinter Version): None (standard library, requires `tkinter`)
  - Pomodoro Timer (Kivy Version): `kivy>=2.0.0`

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ThreeFistfulsofFigs/Python_Beginners_Projects.git
   cd Python_Beginners_Projects
   ```
2. **Set Up Virtual Environment** (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```
3. **Install Dependencies**:
   - For Currency Converter:
     ```bash
     pip install requests
     ```
   - For EPUB to PDF Converter:
     ```bash
     pip install ebooklib beautifulsoup4 pdfkit
     ```
     Install `wkhtmltopdf`:
     - **Windows**: Download from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html).
     - **Linux**: `sudo apt-get install wkhtmltopdf`
     - **macOS**: `brew install wkhtmltopdf`
   - For Markdown to PDF Converter:
     ```bash
     pip install markdown2 pdfkit
     ```
     Install `wkhtmltopdf`:
     - **Windows**: Download from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html).
     - **Linux**: `sudo apt-get install wkhtmltopdf`
     - **macOS**: `brew install wkhtmltopdf`
   - For VPN Kill Switch Configuration Tool:
     ```bash
     pip install psutil pywin32
     ```
   - For Modern Art Painting Generator:
     ```bash
     pip install Pillow
     ```
   - For Snake Game:
     - Install `tkinter` on Linux if needed:
       ```bash
       sudo apt-get install python3-tk
       ```
   - For Pong Game:
     - Install `tkinter` on Linux if needed:
       ```bash
       sudo apt-get install python3-tk
       ```
   - For Pomodoro Timer (Tkinter Version):
     - Install `tkinter` on Linux if needed:
       ```bash
       sudo apt-get install python3-tk
       ```
   - For Pomodoro Timer (Kivy Version):
     - Install `kivy`:
       ```bash
       pip install kivy
       ```
     - On Linux, install Kivy dependencies if needed:
       ```bash
       sudo apt-get install python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
       ```
   - Word Frequency Analyzer, Text Analyzer, Morse Code Converter, ChatBot, Quiz Game, Random Turtle Walk, and Colorful Spirograph require no additional packages.

### Exploring Projects
1. Navigate to a project folder (e.g., `cd chatbot`, `cd md_to_pdf_converter`, `cd blackjack`, `cd quiz_game`, `cd random_turtle_walk`, `cd colorful_spirograph`, `cd modern_art_painting_generator`, `cd snake_game`, `cd pong_game`, `cd pomodoro_timer`, `cd pomodoro_timer_kivy`).
2. Read the project-specific `README.md` for detailed setup and usage instructions.
3. Run the project’s `main.py`:
   ```bash
   python main.py
   ```
4. Follow prompts or interact with the GUI as described in each project’s README.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Add or enhance a project, ensuring it includes a `main.py` and `README.md` with setup, usage, and troubleshooting sections.
4. Commit changes: `git commit -m "Add your feature"`.
5. Push to your fork: `git push origin feature/your-feature`.
6. Open a pull request on [GitHub](https://github.com/ThreeFistfulsofFigs/Python_Beginners_Projects).
7. Report issues or suggestions via the repository’s Issues page.

## Troubleshooting

### General Issues
- **Python Not Found**:
  - Ensure Python 3.7+ is installed: `python --version`.
  - Add Python to PATH or use full path (e.g., `/usr/bin/python3`).
- **Module Not Found**:
  - Install missing dependencies (e.g., `pip install requests`).
  - Verify virtual environment is activated.
  - Ensure the correct Python environment is used (e.g., run `python -m pip install <package>` to match the interpreter).

### Project-Specific Issues
- **Currency Converter**:
  - **API Errors**: Ensure a valid freecurrencyapi.com API key is set in `main.py`.
  - **Offline Mode**: Verify `rates.json` exists for fallback.
- **EPUB to PDF Converter**:
  - **wkhtmltopdf Not Found**: Install `wkhtmltopdf` and verify path.
  - **GUI Issues**: Ensure `tkinter` is installed (`sudo apt-get install python3-tk` on Linux).
- **Markdown to PDF Converter**:
  - **wkhtmltopdf Not Found**: Install `wkhtmltopdf` and verify path.
  - **GUI Issues**: Ensure `tkinter` is installed (`sudo apt-get install python3-tk` on Linux).
- **Word Frequency Analyzer**:
  - **File Errors**: Ensure valid `.txt` files are used and check file permissions.
  - **GUI Issues**: Ensure `tkinter` is installed (`sudo apt-get install python3-tk` on Linux).
- **Text Analyzer**:
  - **File Encoding Errors**: The tool attempts multiple encodings (UTF-8, Latin-1, CP1252, ISO-8859-1). Check file encoding if errors occur.
  - **GUI Issues**: Ensure `tkinter` is installed (`sudo apt-get install python3-tk` on Linux).
- **VPN Kill Switch Configuration Tool**:
  - **Access Denied Errors**: Run the executable as administrator for network control and installation.
  - **Module Not Found**: Install `psutil` and `pywin32` (`pip install psutil pywin32`).
  - **Network Interface Issues**: Verify interface name with `netsh interface show interface`.
  - **Log File Issues**: Check `%USERPROFILE%\vpn_killswitch.log` for errors.
- **Morse Code Converter**:
  - **Invalid Input Errors**: Ensure text contains only supported characters (letters, numbers, listed symbols). For Morse code, use dots (.), dashes (-), single spaces between letters, and double spaces between words.
  - **Empty Input**: Enter non-empty text or Morse code when prompted.
- **ChatBot**:
  - **No Response or "Sorry, I didn't understand you"**: Ensure input is similar to patterns in `responses.json` (e.g., "hello", "what time is it?"). The similarity threshold requires a close match.
  - **Empty Input**: Enter non-empty text when prompted.
  - **File Not Found Error**: Ensure `responses.json` exists in the `chatbot` directory.
  - **Invalid JSON Format**: Verify `responses.json` contains valid JSON (key-value pairs of strings).
- **Blackjack Game**:
  - **Module Not Found**: Ensure the `art.py` file is in the `blackjack` directory, as the project uses a local `art.py` file for graphics, not the PyPI `art` library.
  - **Console Not Clearing**: Verify `os` module support for your platform (Windows: `cls`, Unix-based: `clear`).
  - **Invalid Input**: Use `y` or `n` for gameplay prompts; other inputs may cause unexpected behavior.
- **Quiz Game**:
  - **Invalid Input**: Enter only `True` or `False` (case-insensitive) when prompted. Other inputs may not be validated.
  - **No Questions Displayed**: Ensure `data.py` exists in the `quiz_game` directory and contains valid question data.
  - **File Not Found Error**: Confirm all required files (`main.py`, `question_model.py`, `quiz_brain.py`, `data.py`) are in the `quiz_game` directory.
  - **Unexpected Termination**: Check for syntax errors in `data.py` or ensure question data includes `question` and `correct_answer` keys.
- **Random Turtle Walk**:
  - **GUI Issues**: Ensure `tkinter` is installed, as the `turtle` module relies on it (`sudo apt-get install python3-tk` on Linux).
  - **Window Not Displaying**: Verify Python is configured to display graphical windows (e.g., ensure a display server is running on Linux).
  - **Slow Performance**: The high speed (40) is set, but reduce the number of steps (e.g., from 500 to 200) if performance is an issue.
- **Colorful Spirograph**:
  - **GUI Issues**: Ensure `tkinter` is installed, as the `turtle` module relies on it (`sudo apt-get install python3-tk` on Linux).
  - **Window Not Displaying**: Verify Python is configured to display graphical windows (e.g., ensure a display server is running on Linux).
  - **Slow Performance**: The turtle speed is set to `"fastest"`. If performance is slow, reduce the number of iterations (e.g., from 100 to 50 in `main.py`).
- **Modern Art Painting Generator**:
  - **GUI Issues**: Ensure `tkinter` is installed, as the `turtle` module relies on it (`sudo apt-get install python3-tk` on Linux).
  - **Window Not Displaying**: Verify Python is configured to display graphical windows (e.g., ensure a display server is running on Linux).
  - **Module Not Found**: Install Pillow (`pip install Pillow`).
  - **File Not Saved**: Ensure write permissions in the project directory and check for `temp.eps` cleanup issues.
  - **Commented-Out Color Extraction**: To use the `colorgram` reference, install `colorgram.py` (`pip install colorgram.py`) and provide a valid `image.jpg`.
- **Snake Game**:
  - **GUI Issues**: Ensure `tkinter` is installed, as the `turtle` module relies on it (`sudo apt-get install python3-tk` on Linux).
  - **Window Not Displaying**: Verify Python is configured to display graphical windows (e.g., ensure a display server is running on Linux).
  - **Slow Performance**: Adjust the `time.sleep(0.1)` value in `main.py` to increase or decrease game speed.
  - **No Response to Arrow Keys**: Ensure the game window is focused and verify key bindings in `main.py`.
- **Pong Game**:
  - **GUI Issues**: Ensure `tkinter` is installed, as the `turtle` module relies on it (`sudo apt-get install python3-tk` on Linux).
  - **Window Not Displaying**: Verify Python is configured to display graphical windows (e.g., ensure a display server is running on Linux).
  - **Slow Performance**: Adjust the `time.sleep(0.06)` value in `main.py` to increase or decrease game speed.
  - **No Response to Keys**: Ensure the game window is focused and verify key bindings (W/S for left player, Up/Down for right player) in `main.py`.
  - **File Not Found**: Ensure all required files (`main.py`, `paddle.py`, `ball.py`, `scoreboard.py`) are in the `pong_game` directory.
- **Pomodoro Timer (Tkinter Version)**:
  - **GUI Not Displaying**: Ensure `tkinter` is installed (`sudo apt-get install python3-tk` on Linux).
  - **Sound Issues**: On non-Windows systems, sounds fall back to the system bell (`\a`). Ensure system audio is enabled.
  - **File Errors**: Check write permissions for `pomodoro_settings.json` if saving fails.
  - **Window Not Responding**: Ensure the window is focused for keyboard shortcuts to work.
- **Pomodoro Timer (Kivy Version)**:
  - **GUI Not Displaying**: Ensure `kivy` is installed (`pip install kivy`) and Python is configured for graphical applications (e.g., ensure a display server is running on Linux).
  - **Sound Issues**: On non-Windows systems, sounds fall back to the system bell (`\a`). Ensure system audio is enabled.
  - **File Errors**: Check write permissions for `pomodoro_settings.json` if saving fails.
  - **Window Not Responding**: Ensure the window is focused for keyboard shortcuts to work.
  - **Kivy Installation Issues**: Verify dependencies (SDL2, GLEW, etc.) are installed. On Linux, you may need:
    ```bash
    sudo apt-get install python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
    ```

## Notes
- **Version**: 1.0.0
- **License**: MIT (see LICENSE file).
- **Structure**: Each project is in its own folder with `main.py` and `README.md`.
- **Security**: For Currency Converter, store API keys securely and avoid sharing.
- **Executables**:
  - **Text Analyzer**: Use `auto-py-to-exe` to create a standalone executable (see project-specific README).
  - **VPN Kill Switch Configuration Tool**: Use PyInstaller to build the executable (see project-specific README).
  - **Morse Code Converter**: Can be converted to an executable using PyInstaller (see project-specific README).
  - **ChatBot**: Can be converted to an executable using PyInstaller (see project-specific README).
  - **Markdown to PDF Converter**: Can be converted to an executable using PyInstaller (see project-specific README).
  - **Blackjack Game**: Can be converted to an executable using PyInstaller (see project-specific README).
  - **Quiz Game**: Can be converted to an executable using PyInstaller (see project-specific README).
  - **Random Turtle Walk**: Can be converted to an executable using PyInstaller (see project-specific README).
  - **Colorful Spirograph**: Can be converted to an executable using PyInstaller (see project-specific README).
  - **Modern Art Painting Generator**: Can be converted to an executable using PyInstaller (see project-specific README).
  - **Snake Game**: Can be converted to an executable using PyInstaller (see project-specific README).
  - **Pong Game**: Can be converted to an executable using PyInstaller (see project-specific README).
  - **Pomodoro Timer (Tkinter Version)**: Can be converted to an executable using PyInstaller (see project-specific README).
  - **Pomodoro Timer (Kivy Version)**: Can be converted to an executable using PyInstaller (see project-specific README).

## Contact
For questions or suggestions, open an issue on the [GitHub repository](https://github.com/ThreeFistfulsofFigs/Python_Beginners_Projects) or contact via email: [gerrit.meurer952@dontsp.am](mailto:gerrit.meurer952@dontsp.am).
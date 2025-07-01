# Python Beginners Projects

## Overview
This repository contains a collection of small, standalone Python projects designed for beginners to explore practical programming concepts. Each project solves everyday problems or demonstrates specific Python techniques, making it ideal for learning and experimentation. Projects include tools for currency conversion, expense splitting, financial planning, text editing, password generation, website monitoring, text analysis, word frequency analysis, VPN kill switch configuration, and Morse code conversion.

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

### 11. Morse Code Converter
- **Purpose**: Converts text to Morse code and vice versa, supporting letters, numbers, and common symbols.
- **Features**:
  - Converts text to Morse code with space-separated codes.
  - Converts Morse code to text, handling single and double spaces.
  - Supports uppercase/lowercase letters, numbers, and symbols.
  - Interactive CLI with error handling and continue/exit options.
- **Tech**: Python, `typing`.
- **How to Use**: Run `main.py`, choose to convert text to Morse, Morse to text, or exit, then follow prompts.
- **Directory**: `morse_code_converter`
- **Dependencies**: None (standard library)

## Getting Started

### Prerequisites
- **Python**: 3.7 or higher, installed and added to PATH.
  ```bash
  python --version
  ```
- **External Tool** (for EPUB to PDF Converter): `wkhtmltopdf` (see project-specific README).
- **Dependencies**:
  - Currency Converter: `requests>=2.25.0`
  - EPUB to PDF Converter: `ebooklib>=0.17.1`, `beautifulsoup4>=4.9.0`, `pdfkit>=0.7.0`
  - Word Frequency Analyzer: None (standard library)
  - Text Analyzer: None (standard library)
  - VPN Kill Switch Configuration Tool: `psutil>=5.8.0`, `pywin32>=306`
  - Morse Code Converter: None (standard library)
  - Others: Use standard Python libraries.

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
   - For VPN Kill Switch Configuration Tool:
     ```bash
     pip install psutil pywin32
     ```
   - Word Frequency Analyzer, Text Analyzer, and Morse Code Converter require no additional packages.
   - Other projects require no additional packages.

### Exploring Projects
1. Navigate to a project folder (e.g., `cd morse_code_converter` or `cd text_analyzer`).
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

### Project-Specific Issues
- **Currency Converter**:
  - **API Errors**: Ensure a valid freecurrencyapi.com API key is set in `main.py`.
  - **Offline Mode**: Verify `rates.json` exists for fallback.
- **EPUB to PDF Converter**:
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

## Notes
- **Version**: 1.0.0
- **License**: MIT (see LICENSE file).
- **Structure**: Each project is in its own folder with `main.py` and `README.md`.
- **Security**: For Currency Converter, store API keys securely and avoid sharing.
- **Executables**:
  - **Text Analyzer**: Use `auto-py-to-exe` to create a standalone executable (see project-specific README).
  - **VPN Kill Switch Configuration Tool**: Use PyInstaller to build the executable (see project-specific README).
  - **Morse Code Converter**: Can be converted to an executable using PyInstaller (see project-specific README).

## Contact
For questions or suggestions, open an issue on the [GitHub repository](https://github.com/ThreeFistfulsofFigs/Python_Beginners_Projects) or contact via email: [gerrit.meurer952@dontsp.am](mailto:gerrit.meurer952@dontsp.am).
# Python Beginners Projects

## Overview
This repository contains a collection of small, standalone Python projects designed for beginners to explore practical programming concepts. Each project solves everyday problems or demonstrates specific Python techniques, making it ideal for learning and experimentation. Projects include tools for currency conversion, expense splitting, financial planning, text editing, password generation, website monitoring, and text analysis.

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
   - Other projects require no additional packages.

### Exploring Projects
1. Navigate to a project folder (e.g., `cd currency_converter`).
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
- **Other Projects**: See project-specific `README.md` for detailed troubleshooting.

## Notes
- **Version**: 1.0.0
- **License**: [Specify license, e.g., MIT, or state "See LICENSE file"].
- **Structure**: Each project is in its own folder with `main.py` and `README.md`.
- **Security**: For Currency Converter, store API keys securely and avoid sharing.

## Contact
For questions or suggestions, open an issue on the [GitHub repository](https://github.com/ThreeFistfulsofFigs/Python_Beginners_Projects) or contact via email: [gerrit.meurer952@dontsp.am](mailto:gerrit.meurer952@dontsp.am).
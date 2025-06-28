# EPUB to PDF Converter

## Overview
The EPUB to PDF Converter is a Python GUI application that converts EPUB files to PDF format using `wkhtmltopdf`. It preserves EPUB pagination with chapter breaks, handles images and internal links, and provides a user-friendly Tkinter interface. Suitable for users needing high-quality PDF versions of eBooks.

## Features
- **GUI Interface**: Select EPUB files and output directory via Tkinter.
- **EPUB Processing**: Extracts images, handles links, and applies eBook-optimized styling.
- **PDF Generation**: Uses `wkhtmltopdf` for high-quality PDF output.
- **Logging**: Displays detailed conversion logs in GUI.
- **Progress Feedback**: Shows progress bar and status updates during conversion.
- **Error Handling**: Manages missing dependencies and conversion errors gracefully.

## Requirements
- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.7 or higher
- **Dependencies**:
  - `ebooklib>=0.17.1`
  - `beautifulsoup4>=4.9.0`
  - `pdfkit>=0.7.0`
  - Built-in: `tkinter`, `os`, `threading`, `tempfile`, `shutil`, `time`
- **External Tool**: `wkhtmltopdf` (must be installed separately)

## Installation

### Step 1: Set Up Environment
1. **Install Python**: Ensure Python 3.7+ is installed and added to PATH.
   ```bash
   python --version
   ```
2. **Install wkhtmltopdf**:
   - **Windows**: Download from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html).
   - **Linux**: `sudo apt-get install wkhtmltopdf`
   - **macOS**: `brew install wkhtmltopdf`
3. **Create Virtual Environment** (optional but recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```
4. **Install Dependencies**:
   ```bash
   pip install ebooklib beautifulsoup4 pdfkit
   ```

### Step 2: Run the Application
1. **Locate Script**: Navigate to the project directory containing `main.py`.
2. **Run the Script**:
   ```bash
   python main.py
   ```
3. **Verify GUI**:
   - GUI opens with fields for EPUB file and output directory.
   - Log window shows `wkhtmltopdf` detection status.

## Usage

### Step 1: Convert an EPUB File
1. **Select EPUB File**: Click "Browse" to choose an `.epub` file.
2. **Select Output Directory**: Click "Browse" to set output folder (defaults to EPUB file’s directory).
3. **Start Conversion**: Click "Convert to PDF" to begin.
4. **Monitor Progress**:
   - Progress bar activates during conversion.
   - Log window shows steps (e.g., "Loading EPUB file...", "Generating PDF...").
5. **Verify Output**:
   - PDF is saved as `[title].pdf` in the output directory.
   - Success message confirms completion.

### Step 2: Testing
1. **Test Conversion**:
   - Select a valid `.epub` file and output directory.
   - Verify PDF is created with correct title and pagination.
   - Check log for messages like:
     ```
     wkhtmltopdf found at: /usr/bin/wkhtmltopdf
     PDF created successfully! Size: 1234567 bytes
     ```
2. **Test Error Handling**:
   - Select invalid EPUB file to confirm error message.
   - Remove `wkhtmltopdf` to verify dependency warning.

## Troubleshooting

### "wkhtmltopdf not found"
- Install `wkhtmltopdf` (see Requirements).
- Verify path in log (e.g., `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`).
- Add `wkhtmltopdf` to PATH if not detected.

### "Missing required library"
- Install missing modules:
  ```bash
  pip install ebooklib beautifulsoup4 pdfkit
  ```

### "Conversion timed out"
- Check log for errors (e.g., invalid EPUB structure).
- Ensure sufficient disk space in output directory.
- Increase timeout in `main.py` (modify `60` in `check_thread`).

### PDF Formatting Issues
- Hanging titles may occur due to `wkhtmltopdf` limitations.
- Verify CSS in `main.py` for page break settings.

## Files Included
- `main.py`: Core script with GUI and conversion logic.

## Notes
- **Version**: 1.0.0
- **Limitations**: Hanging titles may persist due to `wkhtmltopdf` constraints.
- **Platform**: Cross-platform, but `wkhtmltopdf` installation varies.

## Support
For issues, check GUI log or submit an issue at [GitHub repository URL] (replace with your repo URL).
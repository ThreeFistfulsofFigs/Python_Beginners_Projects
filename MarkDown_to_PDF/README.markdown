# Markdown to PDF Converter Documentation

## Overview
The Markdown to PDF Converter is a Python-based desktop application that converts Markdown files to PDF documents. It provides a simple graphical user interface for easy file selection and conversion monitoring.

## Features
- Convert Markdown files to PDF format
- User-friendly graphical interface
- Progress tracking during conversion
- Support for common Markdown syntax
- Cancellable conversion process
- Custom PDF styling and formatting
- Support for dark mode with toggle button

## Installation Requirements

### Required Software
1. Python 3.x
2. wkhtmltopdf (Required for PDF generation)
   - Download from: https://wkhtmltopdf.org/downloads.html

### Python Dependencies
```bash
pip install markdown2 pdfkit
```

## Running the Application

### Method 1: Using the Batch File
1. Double-click `Markdown_converter.bat`
2. The application will automatically check for dependencies and launch

### Method 2: Using Python
```bash
python run_markdown_converter.py
```

## Usage Instructions

1. **Launch the Application**
   - Start the program using either method described above
   - The main window will appear with a "Select and Convert" button

2. **Converting Files**
   - Click "Select and Convert"
   - Choose your Markdown (.md) file when prompted
   - Select the destination for your PDF file
   - Wait for the conversion to complete
   - A success message will appear with the PDF location

3. **Monitoring Progress**
   - The progress bar shows conversion status
   - Status messages appear below the progress bar
   - Use the Cancel button to stop the conversion
   - Toggle dark mode using the "Toggle Dark Mode" button

## Project Structure

- [`main.py`](src/main.py): Main application controller
- [`gui.py`](src/gui.py): User interface implementation
- [`converter.py`](src/converter.py): Core conversion logic
- [`run_markdown_converter.py`](src/run_markdown_converter.py): Dependency checker and launcher

## Error Handling

The application handles various error scenarios:
- Missing wkhtmltopdf installation
- Invalid input files
- Permission issues
- Conversion failures
- Missing dependencies

## Supported Markdown Features

- Headers (all levels)
- Bold and italic text
- Code blocks
- Tables
- Lists (ordered and unordered)
- Links
- Images
- Blockquotes

## PDF Output Styling

The generated PDFs include:
- Clean, readable fonts
- Proper margins
- Syntax highlighting for code
- Responsive tables
- Proper image scaling
- A4 page format

## Troubleshooting

1. **wkhtmltopdf not found**
   - Install wkhtmltopdf from the official website
   - Add installation directory to system PATH

2. **Conversion fails**
   - Check input file permissions
   - Verify wkhtmltopdf installation
   - Ensure output directory is writable

3. **Dependencies missing**
   - Run `pip install markdown2 pdfkit`
   - Check Python installation

## Development Notes

- Built using tkinter for cross-platform GUI
- Uses markdown2 for Markdown parsing
- Implements threading to prevent UI freezing
- Includes progress monitoring
- Supports conversion cancellation

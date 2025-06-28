EPUB to PDF Converter
This script provides a graphical user interface (GUI) to convert EPUB files into PDF format using Python. It leverages the Tkinter library for the GUI, ebooklib for EPUB parsing, BeautifulSoup for HTML manipulation, and pdfkit with wkhtmltopdf for PDF generation. The tool preserves EPUB pagination, handles internal links and images, and includes robust error handling and logging.
Features

Converts EPUB files to PDF with chapter breaks aligned to the original EPUB spine.
Extracts and embeds images from the EPUB into the PDF.
Handles internal links and anchors for navigation within the PDF.
Provides a user-friendly GUI with file browsing, progress feedback, and logs.
Optimizes layout with eBook-like styling (e.g., justified text, proper margins).
Includes cleanup of temporary files after conversion.

Limitations

Hanging titles (subtitles on the last line of a page) may persist due to wkhtmltopdf limitations.
The layout consistency is the best achievable balance with the current toolset.

Requirements

Python 3.x
Required Python packages:
ebooklib
beautifulsoup4
pdfkit


wkhtmltopdf installed and accessible:
Windows: Download from https://wkhtmltopdf.org/downloads.html
Linux: sudo apt-get install wkhtmltopdf
macOS: brew install wkhtmltopdf



Installation

Install the required Python packages:pip install ebooklib beautifulsoup4 pdfkit


Install wkhtmltopdf based on your operating system (see above).
Clone or copy the main.py script to your project directory.

Usage

Run the script:python main.py


In the GUI:
Click "Browse" to select an EPUB file.
Click "Browse" to choose an output directory.
Click "Convert to PDF" to start the conversion.


Monitor the progress bar and log window for status updates.
Once complete, a success message will display the saved PDF location.

Notes

The conversion process runs in a separate thread to keep the GUI responsive.
A 60-second timeout is enforced to prevent hangs; adjust if needed by modifying the check_thread method.
Temporary files are cleaned up automatically, but errors during cleanup are logged.

License
[Add your preferred license here, e.g., MIT, GPL, or a custom one.]
Contributing
[Optional: Add guidelines for contributions if you plan to open-source this.]
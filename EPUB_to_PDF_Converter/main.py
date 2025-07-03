# ============================================================================
# EPUB TO PDF CONVERTER
# ============================================================================
# This script converts EPUB files to PDF format using a Tkinter GUI. It processes
# EPUB content, extracts images, handles internal links, and generates a PDF with
# wkhtmltopdf. The styling respects the original EPUB pagination by enforcing page
# breaks at chapter ends, minimizes mid-text breaks, and maintains a consistent
# layout. Note: Hanging titles (subtitles on the last line) may persist due to
# wkhtmltopdf limitations; this is the best achievable balance for now.
# ============================================================================

# Import required libraries
import tkinter as tk  # For GUI creation
from tkinter import filedialog, messagebox, ttk  # For file dialogs and UI components
import os  # For file and directory operations
import threading  # For background conversion to keep UI responsive
import tempfile  # For temporary file management
import shutil  # For directory cleanup
import time  # For delays and timeouts

try:
    import ebooklib  # For reading EPUB files
    from ebooklib import epub  # EPUB-specific functionality
    from bs4 import BeautifulSoup  # For HTML parsing and manipulation
    import pdfkit  # For PDF generation via wkhtmltopdf
except ImportError as e:
    # ERROR FEEDBACK
    # Display installation instructions if dependencies are missing
    messagebox.showerror("Error", f"Missing required library: {e}\n\n"
                                  "Please install required packages:\n"
                                  "pip install ebooklib beautifulsoup4 pdfkit\n\n"
                                  "Also install wkhtmltopdf:\n"
                                  "Windows: Download from https://wkhtmltopdf.org/downloads.html\n"
                                  "Linux: sudo apt-get install wkhtmltopdf\n"
                                  "macOS: brew install wkhtmltopdf")
    exit(1)


# ============================================================================
# WKHTMLTOPDF DETECTION FUNCTION
# ============================================================================

def find_wkhtmltopdf() -> str:
    """
    Locate the wkhtmltopdf executable in common system paths.

    Returns:
        str: Path to wkhtmltopdf executable, or empty string if not found.
    """
    # PATH SEARCH
    # Check common installation paths for wkhtmltopdf
    common_paths = [
        r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
        r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe",
        "/usr/local/bin/wkhtmltopdf",
        "/usr/bin/wkhtmltopdf",
        shutil.which("wkhtmltopdf")
    ]
    for path in common_paths:
        if path and os.path.isfile(path):
            return path
    return ""


# ============================================================================
# EPUB TO PDF CONVERTER CLASS
# ============================================================================

class EPUBtoPDFConverter:
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the EPUB to PDF converter GUI.

        Args:
            root (tk.Tk): The Tkinter root window.
        """
        # GUI SETUP
        # Configure window properties
        self.root = root
        self.root.title("EPUB to PDF Converter")
        self.root.geometry("500x350")
        self.root.resizable(True, True)
        self.epub_file = ""
        self.output_dir = ""
        self.wkhtmltopdf_path = find_wkhtmltopdf()
        self.setup_gui()
        self.check_dependencies()

    def check_dependencies(self) -> None:
        """
        Verify that wkhtmltopdf is installed and log its status.
        """
        # DEPENDENCY CHECK
        # Log wkhtmltopdf availability or provide installation instructions
        if self.wkhtmltopdf_path:
            self.log_message(f"wkhtmltopdf found at: {self.wkhtmltopdf_path}")
            self.log_message("Ready for conversion.")
        else:
            self.log_message("WARNING: wkhtmltopdf not found!")
            self.log_message("Please install wkhtmltopdf:")
            self.log_message("Windows: Download from https://wkhtmltopdf.org/downloads.html")
            self.log_message("Linux: sudo apt-get install wkhtmltopdf")
            self.log_message("macOS: brew install wkhtmltopdf")

    def setup_gui(self) -> None:
        """
        Set up the Tkinter GUI with input fields, buttons, and log display.
        """
        # MAIN FRAME SETUP
        # Create and configure the main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # TITLE LABEL
        # Add a bold title for the application
        title_label = ttk.Label(main_frame, text="EPUB to PDF Converter", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # EPUB FILE INPUT
        # Create input field and browse button for EPUB file
        ttk.Label(main_frame, text="EPUB File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.epub_path_var = tk.StringVar()
        epub_entry = ttk.Entry(main_frame, textvariable=self.epub_path_var, width=40)
        epub_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        epub_browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_epub_file)
        epub_browse_btn.grid(row=1, column=2, padx=(5, 0), pady=5)

        # OUTPUT DIRECTORY INPUT
        # Create input field and browse button for output directory
        ttk.Label(main_frame, text="Output Directory:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.output_path_var = tk.StringVar()
        output_entry = ttk.Entry(main_frame, textvariable=self.output_path_var, width=40)
        output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        output_browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_output_dir)
        output_browse_btn.grid(row=2, column=2, padx=(5, 0), pady=5)

        # CONVERT BUTTON
        # Add button to start conversion
        self.convert_btn = ttk.Button(main_frame, text="Convert to PDF", command=self.start_conversion)
        self.convert_btn.grid(row=3, column=0, columnspan=3, pady=20)

        # PROGRESS BAR
        # Add indeterminate progress bar for conversion feedback
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        # STATUS LABEL
        # Display conversion status
        self.status_var = tk.StringVar(value="Ready to convert")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=5, column=0, columnspan=3, pady=5)

        # LOG FRAME
        # Create a scrollable log window for detailed feedback
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)

        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

    def browse_epub_file(self) -> None:
        """
        Open a file dialog to select an EPUB file and set the output directory.
        """
        # FILE SELECTION
        # Prompt user to select an EPUB file
        file_path = filedialog.askopenfilename(
            title="Select EPUB file",
            filetypes=[("EPUB files", "*.epub"), ("All files", "*.*")]
        )
        if file_path:
            self.epub_file = file_path
            self.epub_path_var.set(file_path)
            if not self.output_dir:
                self.output_dir = os.path.dirname(file_path)
                self.output_path_var.set(self.output_dir)

    def browse_output_dir(self) -> None:
        """
        Open a directory dialog to select the output directory.
        """
        # DIRECTORY SELECTION
        # Prompt user to select an output directory
        dir_path = filedialog.askdirectory(title="Select output directory")
        if dir_path:
            self.output_dir = dir_path
            self.output_path_var.set(dir_path)

    def log_message(self, message: str) -> None:
        """
        Log a message to the GUI's text area and update the display.

        Args:
            message (str): The message to log.
        """
        # LOGGING
        # Append message to log window and scroll to end
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def start_conversion(self) -> None:
        """
        Start the EPUB to PDF conversion in a separate thread.
        """
        # VALIDATION
        # Check for wkhtmltopdf, EPUB file, and output directory
        if not self.wkhtmltopdf_path:
            messagebox.showerror("Error", "wkhtmltopdf not found. Please install wkhtmltopdf.")
            return
        if not self.epub_file or not os.path.exists(self.epub_file):
            messagebox.showerror("Error", "Please select a valid EPUB file")
            return
        if not self.output_dir:
            messagebox.showerror("Error", "Please select an output directory")
            return

        # UI UPDATE
        # Disable button, start progress bar, and launch conversion thread
        self.convert_btn.config(state='disabled')
        self.progress.start()
        self.status_var.set("Converting...")
        thread = threading.Thread(target=self.convert_epub_to_pdf)
        thread.daemon = True
        thread.start()
        self.root.after(100, lambda: self.check_thread(thread, time.time()))

    def check_thread(self, thread, start_time):
        """
        Monitor the conversion thread and handle timeouts.

        Args:
            thread: The running conversion thread.
            start_time: The time the conversion started.
        """
        # THREAD MONITORING
        # Check if thread is still running or has timed out
        if thread.is_alive():
            if time.time() - start_time > 60:  # 60-second timeout
                self.log_message("Conversion timed out after 60 seconds")
                self.status_var.set("Conversion failed")
                self.root.after(0, lambda: messagebox.showerror("Error", "Conversion timed out"))
                thread.join(timeout=1)  # Force join with small timeout
                self.finish_conversion()
            else:
                self.root.after(100, lambda: self.check_thread(thread, start_time))
        else:
            self.finish_conversion()

    def convert_epub_to_pdf(self) -> None:
        """
        Convert the EPUB file to PDF, handling content, images, and links.
        """
        temp_dir = None
        temp_html_path = None
        try:
            # INITIALIZATION
            # Log start of conversion and load EPUB
            self.log_message("Starting conversion...")
            self.log_message("Loading EPUB file...")
            book = epub.read_epub(self.epub_file)
            self.log_message(f"Loaded EPUB: {os.path.basename(self.epub_file)}")

            # METADATA EXTRACTION
            # Extract book title for output file naming
            title = "converted_book"
            if book.get_metadata('DC', 'title'):
                title = book.get_metadata('DC', 'title')[0][0]
                title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            self.log_message(f"Extracted title: {title}")

            # TEMP DIRECTORY SETUP
            # Create temporary directory for images and HTML
            temp_dir = tempfile.mkdtemp()
            self.log_message(f"Created temporary directory: {temp_dir}")

            # IMAGE EXTRACTION
            # Save EPUB images to temporary directory
            self.log_message("Extracting images...")
            image_map = {}
            for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
                image_name = os.path.basename(item.get_name())
                image_path = os.path.join(temp_dir, image_name)
                with open(image_path, 'wb') as f:
                    f.write(item.get_content())
                image_map[item.get_name()] = image_path
            self.log_message(f"Extracted {len(image_map)} images")

            # CONTENT ORDERING
            # Process EPUB content in spine order
            self.log_message("Processing EPUB content using spine...")
            try:
                spine_items = []
                for item_id, _ in book.spine:
                    item = book.get_item_by_id(item_id)
                    if item:
                        spine_items.append(item)
                items = spine_items
                self.log_message(f"Found {len(items)} spine items")
            except:
                items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
                self.log_message(f"Fallback: Found {len(items)} document items")

            # PHASE 1: LINK AND ID MAPPING
            # Build maps for IDs and links to handle internal references
            self.log_message("Phase 1: Building ID and link maps...")
            file_to_index = {}  # Map filename to item index
            all_ids = {}  # Map original_id -> (file_index, new_id)
            all_links = []  # List of (file_index, link_element, original_href)

            for i, item in enumerate(items):
                file_to_index[item.get_name()] = i
                soup = BeautifulSoup(item.get_content(), 'html.parser')

                # ID COLLECTION
                # Find all elements with IDs
                for element in soup.find_all(attrs={'id': True}):
                    original_id = element['id']
                    new_id = f"file{i}_{original_id}"
                    all_ids[original_id] = (i, new_id)
                    self.log_message(f"Found ID: {original_id} -> {new_id} in file {i}")

                # LINK COLLECTION
                # Find all internal links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    all_links.append((i, link, href))

            self.log_message(f"Found {len(all_ids)} unique IDs and {len(all_links)} links")

            # PHASE 2: CONTENT PROCESSING
            # Process content with eBook-optimized styling and chapter breaks
            self.log_message("Phase 2: Processing content with eBook-optimized styling...")

            content_html = ["""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                font-family: 'Palatino Linotype', Palatino, 'Book Antiqua', serif; 
                font-size: 11pt;
                line-height: 1.6; 
                margin: 0.75in;
                color: #000000;
            }

            /* HEADING STYLES */
            /* Clear hierarchy with prevention of hanging titles via text flow */
            h1, h2, h3, h4, h5, h6 { 
                color: #000000; 
                margin: 1.2em 0 0.6em;
                font-weight: normal;
                page-break-inside: avoid;
                page-break-before: avoid;
            }
            h1 { 
                font-size: 18pt; 
                text-align: center;
                margin-top: 1.5em;
            }
            h2 { font-size: 14pt; }
            h3 { font-size: 12pt; }
            h4 { font-size: 11pt; font-style: italic; }
            h5, h6 { font-size: 10pt; }

            /* PARAGRAPH STYLING */
            /* Justified text with indent and enhanced flow control */
            p { 
                margin: 0 0 0.8em 0; 
                text-align: justify;
                text-indent: 1.5em;
                orphans: 3;
                widows: 3;
                page-break-inside: avoid;
            }

            /* TITLE PAGE */
            /* Centered title with significant top margin */
            .title-page {
                text-align: center;
                margin-top: 40%;
                font-size: 20pt;
                page-break-after: always;
            }

            /* CHAPTER STYLING */
            /* Page break before each chapter to match EPUB pagination */
            .chapter {
                page-break-before: always;
                margin-top: 1em;
                padding-top: 1em;
            }

            /* ANCHOR POSITIONING */
            /* Ensure accurate link targets in PDF */
            .anchor-target {
                display: block;
                position: relative;
                top: -60px;
                height: 0;
                visibility: hidden;
            }

            /* IMAGE HANDLING */
            /* Scale images to fit page without breaking */
            img {
                max-width: 85%;
                height: auto;
                display: block;
                margin: 1em auto;
                page-break-inside: avoid;
                page-break-after: avoid;
            }

            /* LINK STYLING */
            /* Subtle links for readability */
            a {
                text-decoration: none;
                color: #003087;
            }
            a:hover {
                text-decoration: underline;
            }

            /* ID ELEMENTS */
            /* Ensure proper positioning for elements with IDs */
            [id] {
                position: relative;
            }

            /* BLOCK ELEMENTS */
            /* Prevent breaks within quotes, code, tables, and lists */
            blockquote, pre, table, ul, ol {
                margin: 1em 0;
                page-break-inside: avoid;
                page-break-after: avoid;
            }

            /* TABLE STYLING */
            /* Clean and minimal table design */
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 1em 0;
                page-break-inside: avoid;
            }
            th, td {
                border: 1px solid #e0e0e0;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f8f8f8;
                font-weight: bold;
            }

            /* LIST STYLING */
            /* Consistent spacing for lists */
            ul, ol {
                padding-left: 2em;
                margin: 1em 0;
            }
            li {
                margin-bottom: 0.5em;
                line-height: 1.6;
            }

            /* PRINT OPTIMIZATIONS */
            /* Adjust margins and anchors for PDF output */
            @media print {
                body { 
                    margin: 0.75in; 
                    font-size: 10.5pt;
                }
                .anchor-target { top: -50px; }
                .chapter { 
                    margin-top: 0.5em; 
                    padding-top: 0.5em; 
                }
            }
        </style>
    </head>
    <body>"""]

            content_html.append(f'<div class="title-page"><h1>{title}</h1></div>')

            for i, item in enumerate(items):
                # CONTENT PROCESSING
                # Process each EPUB item in spine order
                self.log_message(f"Processing item {i + 1}/{len(items)}: {item.get_name()}")
                soup = BeautifulSoup(item.get_content(), 'html.parser')

                # SCRIPT REMOVAL
                # Remove scripts to prevent rendering issues
                for script in soup(["script"]):
                    script.decompose()

                # IMAGE PATH FIXING
                # Update image sources to point to temporary files
                for img in soup.find_all('img'):
                    src = img.get('src')
                    if src:
                        if src.startswith('../'):
                            src = src[3:]
                        if src in image_map:
                            img['src'] = image_map[src]

                # ID HANDLING
                # Update IDs for PDF-compatible anchors
                for element in soup.find_all(attrs={'id': True}):
                    original_id = element['id']
                    if original_id in all_ids:
                        _, new_id = all_ids[original_id]
                        anchor_span = soup.new_tag('span', **{'class': 'anchor-target', 'id': new_id})
                        element.insert_before(anchor_span)
                        del element['id']
                        self.log_message(f"Created anchor target: {original_id} -> {new_id}")

                # LINK HANDLING
                # Fix internal links for PDF navigation
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    original_href = href
                    self.log_message(f"Processing link: {href}")

                    try:
                        if href.startswith('#'):
                            target_id = href[1:]
                            if target_id in all_ids:
                                _, new_id = all_ids[target_id]
                                link['href'] = f"#{new_id}"
                                self.log_message(f"Updated anchor link: {href} -> #{new_id}")
                            else:
                                self.log_message(f"Warning: Anchor target not found: {target_id}")
                                link['class'] = link.get('class', []) + ['broken-link']

                        elif '#' in href:
                            _, anchor_part = href.split('#', 1)
                            if anchor_part in all_ids:
                                _, new_id = all_ids[anchor_part]
                                link['href'] = f"#{new_id}"
                                self.log_message(f"Updated file+anchor link: {href} -> #{new_id}")
                            else:
                                self.log_message(f"Warning: Cross-file anchor not found: {anchor_part}")
                                link['class'] = link.get('class', []) + ['broken-link']
                        else:
                            if not href.startswith(('http://', 'https://', 'mailto:', 'ftp://')):
                                target_file_index = None
                                for file_name, file_index in file_to_index.items():
                                    if file_name.endswith(href) or href in file_name:
                                        target_file_index = file_index
                                        break
                                if target_file_index is not None:
                                    chapter_id = f"file{target_file_index}_start"
                                    link['href'] = f"#{chapter_id}"
                                    self.log_message(f"Updated file link: {href} -> #{chapter_id}")
                                else:
                                    self.log_message(f"Warning: File target not found: {href}")
                                    link['class'] = link.get('class', []) + ['broken-link']

                    except Exception as e:
                        self.log_message(f"Error processing link {original_href}: {str(e)}")
                        link['class'] = link.get('class', []) + ['broken-link']

                # CHAPTER MARKERS
                # Add chapter divs with anchors
                if i > 0:
                    content_html.append(f'<div class="chapter">')
                    content_html.append(f'<span class="anchor-target" id="file{i}_start"></span>')
                else:
                    content_html.append(f'<div>')
                    content_html.append(f'<span class="anchor-target" id="file{i}_start"></span>')

                # CONTENT INCLUSION
                # Add processed HTML content
                if soup.body:
                    for element in soup.body.children:
                        if element.name:
                            content_html.append(str(element))
                else:
                    content_html.append(str(soup))

                content_html.append('</div>')

            content_html.append("</body></html>")
            full_html = '\n'.join(content_html)

            # TEMP HTML CREATION
            # Write processed content to temporary HTML file
            self.log_message("Creating temporary HTML file...")
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', encoding='utf-8', delete=False) as temp_file:
                temp_file.write(full_html)
                temp_html_path = temp_file.name
            self.log_message(f"Temporary HTML file created: {temp_html_path}")

            # PDF OUTPUT
            # Generate PDF from HTML
            output_path = os.path.join(self.output_dir, f"{title}.pdf")
            self.log_message(f"Generating PDF at: {output_path}")
            os.makedirs(self.output_dir, exist_ok=True)

            # PDF CONFIGURATION
            # Set options for wkhtmltopdf
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'no-outline': None,
                'enable-local-file-access': None,
                'disable-smart-shrinking': None,
                'image-dpi': 300,
                'image-quality': 100,
                'enable-internal-links': None,
                'print-media-type': None,
                'zoom': 1.0,
                'disable-javascript': None,
                'load-error-handling': 'ignore',
                'load-media-error-handling': 'ignore'
            }
            config = pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf_path)

            self.log_message("Starting PDF conversion...")
            try:
                time.sleep(1)
                pdfkit.from_file(temp_html_path, output_path, options=options, configuration=config)
                self.log_message("PDF conversion completed")
            except Exception as e:
                self.log_message(f"PDF conversion failed: {str(e)}")
                raise

            # OUTPUT VERIFICATION
            # Check if PDF was created successfully
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                self.log_message(f"PDF created successfully! Size: {file_size} bytes")
            else:
                raise Exception("PDF file was not created")

            # SUCCESS FEEDBACK
            # Notify user of successful conversion
            self.log_message("Conversion completed successfully!")
            self.status_var.set("Conversion completed")
            self.root.after(0, lambda: messagebox.showinfo(
                "Success",
                f"PDF created successfully!\nSaved as: {output_path}\n\nNote: Chapter breaks and formatting optimized to match EPUB pagination, with improved text flow. Hanging titles may still occur due to wkhtmltopdf limitations."
            ))

        except Exception as e:
            # ERROR HANDLING
            # Log and display any conversion errors
            error_msg = f"Error during conversion: {str(e)}"
            self.log_message(error_msg)
            self.status_var.set("Conversion failed")
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))

        finally:
            # CLEANUP
            # Remove temporary files and directories
            time.sleep(2)
            if temp_html_path and os.path.exists(temp_html_path):
                try:
                    os.unlink(temp_html_path)
                    self.log_message("Cleaned up temporary HTML file")
                except OSError as e:
                    self.log_message(f"Error cleaning up temp file: {e}")
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    self.log_message("Cleaned up temporary directory")
                except OSError as e:
                    self.log_message(f"Error cleaning up temp directory: {e}")
            self.root.after(0, self.finish_conversion)

    def finish_conversion(self) -> None:
        """
        Finalize the conversion process by resetting the UI.
        """
        # UI RESET
        # Stop progress bar and re-enable convert button
        self.progress.stop()
        self.convert_btn.config(state='normal')


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================

def main() -> None:
    """
    Main function to launch the EPUB to PDF converter GUI.
    """
    # GUI INITIALIZATION
    # Create and run the Tkinter application
    root = tk.Tk()
    EPUBtoPDFConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()

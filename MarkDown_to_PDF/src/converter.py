# ============================================================================
# MARKDOWN TO PDF CONVERSION LOGIC
# ============================================================================
# This module contains the MarkdownConverter class, responsible for converting
# Markdown files to PDF format using markdown2 and pdfkit libraries. It handles
# file reading, HTML generation, and PDF conversion with progress updates.
# ============================================================================

# Import required libraries
import markdown2          # For converting Markdown to HTML
import pdfkit             # For converting HTML to PDF
import os                 # For file and directory operations
import subprocess         # For executing system commands to locate wkhtmltopdf
import tempfile           # For creating temporary directories and files
import shutil             # For file copying and directory cleanup
from pathlib import Path  # For cross-platform file path handling
from config import DEFAULT_CONFIG  # Import default PDF configuration settings

# ============================================================================
# MARKDOWN CONVERTER CLASS
# ============================================================================
class MarkdownConverter:
    def __init__(self, gui):
        """
        Initialize the MarkdownConverter with a reference to the GUI.

        Args:
            gui (ConverterGUI): The GUI instance for displaying status and progress

        Returns:
            None: Initializes the converter with wkhtmltopdf path and GUI reference
        """
        # GUI REFERENCE
        # Store the GUI instance for status and progress updates
        self.gui = gui
        # CANCELLATION FLAG
        # Flag to track if conversion should be cancelled
        self.cancelled = False
        # WKHTMLTOPDF PATH
        # Locate and store the path to wkhtmltopdf executable
        self.wkhtmltopdf_path = self._find_wkhtmltopdf()
        print(f"Using wkhtmltopdf path: {self.wkhtmltopdf_path}")

    def _find_wkhtmltopdf(self):
        """
        Locate the wkhtmltopdf executable on the system.

        Returns:
            str or None: Path to wkhtmltopdf executable if found, else None
        """
        # CHECK ENVIRONMENT VARIABLE
        # Look for WKHTMLTOPDF_PATH environment variable
        env_path = os.environ.get('WKHTMLTOPDF_PATH')
        if env_path and os.path.isfile(env_path):
            print(f"Found wkhtmltopdf via WKHTMLTOPDF_PATH: {env_path}")
            return env_path

        # CHECK COMMON PATHS
        # List of common installation paths for wkhtmltopdf
        possible_paths = [
            r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe',      # Default Windows path
            r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe', # 32-bit Windows path
            r'C:\wkhtmltopdf\bin\wkhtmltopdf.exe',                    # Alternative Windows path
            '/usr/local/bin/wkhtmltopdf',                              # macOS/Linux path
            '/usr/bin/wkhtmltopdf',                                    # Linux path
        ]
        for path in possible_paths:
            if os.path.isfile(path):
                print(f"Found wkhtmltopdf at: {path}")
                return path

        # CHECK PDFKIT CONFIGURATION
        # Attempt to get wkhtmltopdf path from pdfkit configuration
        try:
            path = pdfkit.configuration().wkhtmltopdf.decode('utf-8')
            print(f"Found wkhtmltopdf via pdfkit: {path}")
            return path
        except Exception as e:
            print(f"Error getting wkhtmltopdf from pdfkit config: {str(e)}")

        # CHECK SYSTEM PATH
        # Use system commands to locate wkhtmltopdf in PATH
        try:
            cmd = 'where' if os.name == 'nt' else 'which'
            result = subprocess.run([cmd, 'wkhtmltopdf'], check=True, stdout=subprocess.PIPE, text=True)
            path = result.stdout.strip().split('\n')[0]
            print(f"Found wkhtmltopdf in PATH: {path}")
            return path
        except Exception as e:
            print(f"Error finding wkhtmltopdf in PATH: {str(e)}")
            return None

    def cancel(self):
        """
        Cancel the current conversion process.

        Returns:
            None: Sets the cancellation flag to stop conversion
        """
        # SET CANCELLATION FLAG
        # Signal that the conversion should be stopped
        self.cancelled = True

    def check_dependencies(self):
        """
        Verify that wkhtmltopdf is installed and accessible.

        Returns:
            bool: True if wkhtmltopdf is found, raises RuntimeError otherwise
        """
        # DEPENDENCY CHECK
        # Ensure wkhtmltopdf is available before proceeding
        if not self.wkhtmltopdf_path:
            raise RuntimeError(
                "wkhtmltopdf not found. Please install it from https://wkhtmltopdf.org/downloads.html"
            )
        return True

    def convert(self, input_file, output_file):
        """
        Convert a Markdown file to PDF with progress updates.

        Args:
            input_file (str): Path to the input Markdown file
            output_file (str): Path where the output PDF will be saved

        Returns:
            bool: True if conversion is successful, False if cancelled or failed
        """
        # TEMPORARY DIRECTORY SETUP
        # Initialize variable for temporary directory
        temp_dir = None
        try:
            # INITIALIZE CONVERSION
            # Reset cancellation flag and update GUI
            self.cancelled = False
            self.gui.show_status("Checking dependencies...")
            self.gui.update_progress(10)
            self.check_dependencies()

            # CHECK FOR CANCELLATION
            # Stop if user cancelled the operation
            if self.cancelled:
                return False

            # CREATE TEMPORARY DIRECTORY
            # Create a temporary directory for intermediate files
            temp_dir = tempfile.mkdtemp(prefix="mdconv_")
            print(f"Created temporary directory: {temp_dir}")

            # READ MARKDOWN FILE
            # Read the content of the input Markdown file
            self.gui.show_status("Reading markdown file...")
            self.gui.update_progress(20)
            content = self.read_file(input_file)

            # CHECK FOR CANCELLATION
            # Stop if user cancelled the operation
            if self.cancelled:
                return False

            # CONVERT MARKDOWN TO HTML
            # Transform Markdown content to HTML with table and code support
            self.gui.show_status("Converting markdown to HTML...")
            self.gui.update_progress(40)
            html = markdown2.markdown(content, extras=['tables', 'code-friendly'])

            # GENERATE HTML WITH STYLING
            # Create HTML with embedded CSS for PDF formatting
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20mm; }}
                    h1, h2, h3, h4, h5, h6 {{ color: #333; }}
                    pre, code {{ background: #f4f4f4; padding: 5px; border-radius: 3px; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; }}
                    img {{ max-width: 100%; height: auto; }}
                </style>
            </head>
            <body>
                {html}
            </body>
            </html>
            """

            # CHECK FOR CANCELLATION
            # Stop if user cancelled the operation
            if self.cancelled:
                return False

            # WRITE HTML TO TEMPORARY FILE
            # Save the generated HTML to a temporary file
            temp_html_path = os.path.join(temp_dir, "input.html")
            self.gui.show_status("Creating HTML file...")
            self.gui.update_progress(60)
            with open(temp_html_path, 'w', encoding='utf-8') as f:
                f.write(html)

            # CHECK FOR CANCELLATION
            # Stop if user cancelled the operation
            if self.cancelled:
                return False

            # CONVERT HTML TO PDF
            # Generate PDF from HTML using wkhtmltopdf
            self.gui.show_status("Converting HTML to PDF...")
            self.gui.update_progress(80)
            temp_output_file = os.path.join(temp_dir, "output.pdf")

            # APPLY PDF CONFIGURATION
            # Use default configuration for PDF settings
            options = DEFAULT_CONFIG
            success = False
            try:
                # PRIMARY CONVERSION ATTEMPT
                # Use pdfkit with wkhtmltopdf configuration
                if self.wkhtmltopdf_path and self.wkhtmltopdf_path != 'wkhtmltopdf':
                    config = pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf_path)
                    pdfkit.from_file(temp_html_path, temp_output_file, options=options, configuration=config)
                else:
                    pdfkit.from_file(temp_html_path, temp_output_file, options=options)
                success = True
            except Exception as e:
                print(f"First conversion attempt failed: {str(e)}")
                # FALLBACK CONVERSION ATTEMPT
                # Try direct wkhtmltopdf command if pdfkit fails
                try:
                    self.gui.show_status("Trying alternative conversion method...")
                    cmd = [
                        self.wkhtmltopdf_path,
                        '--page-size', options['page_size'],
                        '--margin-top', options['margin_top'],
                        '--margin-right', options['margin_right'],
                        '--margin-bottom', options['margin_bottom'],
                        '--margin-left', options['margin_left'],
                        '--encoding', options['encoding'],
                        temp_html_path,
                        temp_output_file
                    ]
                    print(f"Running command: {' '.join(cmd)}")
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode != 0:
                        raise RuntimeError(f"wkhtmltopdf command failed: {result.stderr}")
                    success = True
                except Exception as e2:
                    raise RuntimeError(f"All conversion attempts failed: {str(e)} and {str(e2)}")

            # VERIFY PDF OUTPUT
            # Check if PDF was created successfully
            if success and os.path.exists(temp_output_file):
                output_dir = os.path.dirname(os.path.abspath(output_file))
                os.makedirs(output_dir, exist_ok=True)
                shutil.copy2(temp_output_file, output_file)
                print(f"Successfully copied PDF from {temp_output_file} to {output_file}")
            else:
                raise RuntimeError("PDF was not created successfully")

            # CONVERSION SUCCESS
            # Update GUI with success message and complete progress
            self.gui.show_status("Conversion completed successfully!")
            self.gui.update_progress(100)
            from tkinter.messagebox import showinfo
            showinfo("Conversion Complete", f"PDF saved to:\n{output_file}")
            return True

        except Exception as e:
            # ERROR HANDLING
            # Display error message and reset progress
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            self.gui.show_status(error_msg)
            self.gui.update_progress(0)
            from tkinter.messagebox import showerror
            showerror("Conversion Error", f"Failed to convert: {str(e)}")
            return False
        finally:
            # CLEANUP TEMPORARY DIRECTORY
            # Remove temporary directory if it exists
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                    print(f"Cleaned up temporary directory: {temp_dir}")
                except Exception as e:
                    print(f"Error cleaning up temporary directory: {str(e)}")

    def read_file(self, input_file):
        """
        Read the content of a Markdown file.

        Args:
            input_file (str): Path to the Markdown file to read

        Returns:
            str: Content of the file as a string
        """
        # READ FILE WITH UTF-8 ENCODING
        # Attempt to read file with UTF-8 encoding first
        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # FALLBACK TO LATIN-1 ENCODING
            # Use latin-1 encoding if UTF-8 fails
            with open(input_file, 'r', encoding='latin-1') as file:
                return file.read()

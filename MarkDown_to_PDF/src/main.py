# ============================================================================
# MARKDOWN TO PDF CONVERTER APPLICATION
# ============================================================================
# This module defines the MarkdownConverterApp class, which integrates the GUI
# and conversion logic to provide a complete Markdown to PDF conversion application.
# It handles file selection, threading for conversion, and user interaction.
#
# IMPORTANT: For proper execution, run this application using
# `python src/run_markdown_converter.py` or `Markdown_converter.bat`
# to ensure dependencies and environment are correctly set up.
# ============================================================================

# Import required libraries
from gui import ConverterGUI            # For the graphical user interface
from src.converter import MarkdownConverter  # For Markdown to PDF conversion logic
from tkinter import filedialog, messagebox  # For file dialogs and error messages
import os                              # For file and directory operations
import threading                       # For running conversion in a separate thread
import webbrowser                      # For opening web pages (e.g., for wkhtmltopdf download)

# ============================================================================
# CUSTOM EXCEPTION FOR CONVERSION ERRORS
# ============================================================================
class ConversionError(Exception):
    """
    Custom exception for handling conversion-related errors.

    Attributes:
        message (str): Error message describing the conversion failure
    """
    pass

# ============================================================================
# MAIN APPLICATION CLASS
# ============================================================================
class MarkdownConverterApp:
    def __init__(self):
        """
        Initialize the Markdown to PDF Converter application.

        Returns:
            None: Sets up the GUI and converter instances
        """
        # GUI INITIALIZATION
        # Create the graphical user interface
        self.gui = ConverterGUI()
        # CONVERTER INITIALIZATION
        # Create the Markdown converter with GUI reference
        self.converter = MarkdownConverter(self.gui)
        # CONFIGURE CONVERT BUTTON
        # Link the convert button to the file selection method
        self.gui.convert_btn.config(command=self.select_files)

        # CONFIGURE CANCEL BUTTON
        # Link the cancel button to the cancellation method if available
        if hasattr(self.gui, 'cancel_btn'):
            self.gui.cancel_btn.config(command=self.cancel_conversion)

        # CONVERSION STATE
        # Track whether a conversion is in progress
        self.conversion_in_progress = False
        # CONVERSION THREAD
        # Store the thread for the conversion process
        self.conversion_thread = None

    def cancel_conversion(self):
        """
        Cancel the ongoing conversion process.

        Returns:
            None: Stops the conversion and resets the GUI
        """
        # CHECK CONVERSION STATUS
        # Only proceed if a conversion is in progress
        if self.conversion_in_progress:
            # STOP CONVERSION
            # Set flags and update GUI to indicate cancellation
            self.conversion_in_progress = False
            self.gui.status_label.config(text="Conversion cancelled")
            self.gui.progress['value'] = 0
            self.gui.convert_btn.config(state='normal')
            if hasattr(self.gui, 'cancel_btn'):
                self.gui.cancel_btn.config(state='disabled')

            # SIGNAL CONVERTER
            # Notify the converter to stop processing
            if hasattr(self.converter, 'cancel'):
                self.converter.cancel()

    def run_conversion(self, input_file, output_file):
        """
        Run the conversion process in a separate thread.

        Args:
            input_file (str): Path to the input Markdown file
            output_file (str): Path where the output PDF will be saved

        Returns:
            None: Executes the conversion and updates the GUI
        """
        try:
            # EXECUTE CONVERSION
            # Call the converter to process the Markdown file
            success = self.converter.convert(input_file, output_file)

            # CHECK CONVERSION RESULT
            # Update GUI if conversion failed or was cancelled
            if not success:
                self.gui.status_label.config(text="Conversion failed or was cancelled")

        except Exception as e:
            # ERROR HANDLING
            # Display any unhandled exceptions during conversion
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            self.gui.status_label.config(text=error_msg)
            messagebox.showerror("Conversion Error", f"An unexpected error occurred: {str(e)}")

        finally:
            # RESET UI STATE
            # Ensure buttons and state are reset after conversion
            self.conversion_in_progress = False
            self.gui.convert_btn.config(state='normal')
            if hasattr(self.gui, 'cancel_btn'):
                self.gui.cancel_btn.config(state='disabled')

    def select_files(self):
        """
        Handle file selection and start the conversion process.

        Returns:
            None: Opens file dialogs and initiates conversion in a thread
        """
        # CHECK CONVERSION STATUS
        # Prevent starting a new conversion if one is in progress
        if self.conversion_in_progress:
            return

        try:
            # CHECK WKHTMLTOPDF
            # Verify wkhtmltopdf is available before proceeding
            if not self.converter.wkhtmltopdf_path:
                if messagebox.askyesno("Dependency Missing",
                                       "wkhtmltopdf not found, which is required for PDF conversion.\n\n"
                                       "Would you like to open the download page?"):
                    webbrowser.open("https://wkhtmltopdf.org/downloads.html")
                return

            # INITIALIZE FILE SELECTION
            # Update GUI to indicate file selection is in progress
            self.gui.status_label.config(text="Selecting files...")
            self.gui.progress['value'] = 0
            self.gui.root.update()

            # SELECT INPUT FILE
            # Open dialog to choose the Markdown file
            input_file = filedialog.askopenfilename(
                title="Select Markdown file",
                filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*")]
            )

            # VALIDATE INPUT FILE
            # Check if a file was selected
            if not input_file:
                self.gui.status_label.config(text="No input file selected")
                return

            # CHECK FILE EXISTENCE
            # Ensure the input file exists and is readable
            if not os.path.isfile(input_file):
                raise ConversionError("Input file does not exist")

            if not os.access(input_file, os.R_OK):
                raise ConversionError(f"Cannot read input file: {input_file}")

            # SET DEFAULT OUTPUT FILE
            # Generate default PDF filename based on input file
            default_output = os.path.splitext(input_file)[0] + ".pdf"

            # SELECT OUTPUT FILE
            # Open dialog to choose where to save the PDF
            output_file = filedialog.asksaveasfilename(
                title="Save PDF as",
                defaultextension=".pdf",
                initialfile=os.path.basename(default_output),
                filetypes=[("PDF files", "*.pdf")]
            )

            # CHECK OUTPUT FILE
            # Ensure an output file was selected
            if not output_file:
                self.gui.status_label.config(text="Conversion cancelled")
                return

            # DEBUG OUTPUT
            # Print file paths for debugging purposes
            print(f"Input file: {input_file}")
            print(f"Output file: {output_file}")

            # VALIDATE OUTPUT DIRECTORY
            # Ensure the output directory is writable
            if output_file:
                output_dir = os.path.dirname(os.path.abspath(output_file))
                if not os.path.exists(output_dir):
                    try:
                        os.makedirs(output_dir, exist_ok=True)
                    except Exception as e:
                        raise ConversionError(f"Cannot create output directory: {output_dir}. Error: {str(e)}")

                if not os.access(output_dir, os.W_OK):
                    raise ConversionError(f"Cannot write to output directory: {output_dir}")

            # START CONVERSION
            # Disable convert button and enable cancel button
            self.conversion_in_progress = True
            self.gui.convert_btn.config(state='disabled')
            if hasattr(self.gui, 'cancel_btn'):
                self.gui.cancel_btn.config(state='normal')

            # RUN CONVERSION IN THREAD
            # Start conversion in a separate thread to avoid freezing the UI
            self.conversion_thread = threading.Thread(
                target=self.run_conversion,
                args=(input_file, output_file)
            )
            self.conversion_thread.daemon = True
            self.conversion_thread.start()

        except ConversionError as e:
            # HANDLE CONVERSION ERRORS
            # Display specific conversion-related errors
            messagebox.showerror("Conversion Error", str(e))
            self.gui.status_label.config(text="Conversion failed!")
            self.gui.progress['value'] = 0
            self.conversion_in_progress = False
            self.gui.convert_btn.config(state='normal')
            if hasattr(self.gui, 'cancel_btn'):
                self.gui.cancel_btn.config(state='disabled')

        except Exception as e:
            # HANDLE UNEXPECTED ERRORS
            # Display any other unexpected errors
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            self.gui.status_label.config(text="Operation failed!")
            self.gui.progress['value'] = 0
            self.conversion_in_progress = False
            self.gui.convert_btn.config(state='normal')
            if hasattr(self.gui, 'cancel_btn'):
                self.gui.cancel_btn.config(state='disabled')

    def run(self):
        """
        Start the application and display the GUI.

        Returns:
            None: Launches the main application loop
        """
        # CHECK DEPENDENCIES AT STARTUP
        # Warn if wkhtmltopdf is not found
        if not self.converter.wkhtmltopdf_path:
            self.gui.status_label.config(
                text="Warning: wkhtmltopdf not found. PDF conversion may fail."
            )
            print("WARNING: wkhtmltopdf not found. You need to install it for this application to work.")
            print("Download it from: https://wkhtmltopdf.org/downloads.html")
        else:
            print(f"Using wkhtmltopdf: {self.converter.wkhtmltopdf_path}")

        # START MAIN LOOP
        # Launch the tkinter main event loop
        self.gui.root.mainloop()

# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    # Execute the application only when script is run directly
    # WARNING: Run this application using `python src/run_markdown_converter.py`
    # or `Markdown_converter.bat` for proper dependency setup
    app = MarkdownConverterApp()
    app.run()

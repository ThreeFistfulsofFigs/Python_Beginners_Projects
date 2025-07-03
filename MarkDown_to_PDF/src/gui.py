# ============================================================================
# GRAPHICAL USER INTERFACE FOR MARKDOWN TO PDF CONVERTER
# ============================================================================
# This module defines the ConverterGUI class, which provides a graphical
# interface for the Markdown to PDF Converter using tkinter. It includes
# buttons for conversion, cancellation, a progress bar, and a button to toggle
# dark mode support.
# ============================================================================

# Import required libraries
import tkinter as tk            # For GUI components
from tkinter import ttk        # For themed widgets
from tkinter import filedialog  # For file selection dialogs
from tkinter.messagebox import showerror  # For error message dialogs

# ============================================================================
# CONVERTER GUI CLASS
# ============================================================================
class ConverterGUI:
    def __init__(self):
        """
        Initialize the GUI for the Markdown to PDF Converter.

        Returns:
            None: Sets up the main window and UI components
        """
        # MAIN WINDOW SETUP
        # Create and configure the main application window
        self.root = tk.Tk()
        print(f"Root window created: {self.root}")  # Debug: Confirm root initialization
        self.root.title("Markdown to PDF Converter")
        self.root.geometry("450x350")  # Increased size to ensure visibility
        self.root.resizable(False, False)

        # STYLE CONFIGURATION
        # Configure styles for buttons, labels, and other widgets
        self.style = ttk.Style()
        self.style.theme_use('default')  # Set theme before defining layouts

        # BASIC STYLES
        self.style.configure('TButton', padding=10)
        self.style.configure('TLabel', font=('Helvetica', 10))

        # DARK MODE STYLES
        self.style.configure('Dark.TButton', background='#444', foreground='white')
        self.style.configure('Dark.TLabel', background='#2e2e2e', foreground='white')
        self.style.configure('Dark.TFrame', background='#2e2e2e')
        self.style.configure('Dark.TEntry', background='#2e2e2e', foreground='white', fieldbackground='#444')
        self.style.configure('Dark.TText', background='#2e2e2e', foreground='white')

        # CONFIGURE DARK PROGRESS BAR STYLE
        # Define layout for Dark.TProgressbar based on Horizontal.TProgressbar
        self.style.layout('Dark.TProgressbar',
                         [('Horizontal.TProgressbar.trough',
                           {'children': [('Horizontal.TProgressbar.pbar',
                                          {'side': 'left', 'sticky': 'ns'})],
                            'sticky': 'nswe'})])
        self.style.configure('Dark.TProgressbar', background='#444', troughcolor='#2e2e2e', foreground='#00ff00')

        # UI SETUP
        # Initialize the user interface components
        self.setup_ui()

        # DARK MODE STATE
        # Track the current dark mode state
        self.is_dark_mode = False

    def setup_ui(self):
        """
        Set up the user interface components for the converter.

        Returns:
            None: Creates and arranges UI elements in the main window
        """
        # MAIN FRAME
        # Create a frame to hold all UI components
        self.main_frame = ttk.Frame(self.root, padding="20", style='TFrame')
        print(f"Main frame created: {self.main_frame}")  # Debug: Confirm frame initialization
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # TITLE LABEL
        # Display the application title
        self.title_label = ttk.Label(
            self.main_frame,
            text="Convert Markdown to PDF",
            font=('Helvetica', 14, 'bold'),
            style='TLabel'
        )
        self.title_label.pack(pady=10)

        # CONVERT BUTTON
        # Button to initiate file selection and conversion
        self.convert_btn = ttk.Button(
            self.main_frame,
            text="Select and Convert",
            style='TButton'
        )
        self.convert_btn.pack(pady=20)

        # CANCEL BUTTON
        # Button to cancel ongoing conversion, initially disabled
        self.cancel_btn = ttk.Button(
            self.main_frame,
            text="Cancel",
            state='disabled',
            style='TButton'
        )
        self.cancel_btn.pack(pady=5)

        # PROGRESS BAR
        # Progress bar to show conversion progress
        self.progress = ttk.Progressbar(
            self.main_frame,
            length=300,
            mode='determinate',
            style='TProgressbar'
        )
        self.progress.pack(pady=10)

        # STATUS LABEL
        # Label to display current status of the conversion
        self.status_label = ttk.Label(
            self.main_frame,
            text="Ready",
            style='TLabel'
        )
        self.status_label.pack(pady=10)

        # TOGGLE DARK MODE BUTTON
        # Button to toggle between dark and light mode
        self.dark_mode_btn = ttk.Button(
            self.main_frame,
            text="Toggle Dark Mode",
            command=self.toggle_dark_mode,
            style='TButton'
        )
        print(f"Dark mode button created: {self.dark_mode_btn}")  # Debug: Confirm button initialization
        self.dark_mode_btn.pack(pady=5)

    def show_status(self, message):
        """
        Update the status label with the given message.

        Args:
            message (str): The status message to display

        Returns:
            None: Updates the status label and refreshes the UI
        """
        # UPDATE STATUS LABEL
        # Display the provided status message
        self.status_label.config(text=message)
        self.root.update()

    def update_progress(self, value):
        """
        Update the progress bar with a value between 0 and 100.

        Args:
            value (float): Progress value (0-100)

        Returns:
            None: Updates the progress bar and refreshes the UI
        """
        # UPDATE PROGRESS BAR
        # Set the progress bar to the specified value
        self.progress['value'] = value
        self.root.update()

    def toggle_dark_mode(self):
        """
        Toggle between dark and light mode for the GUI.

        Returns:
            None: Changes the GUI colors and styles based on current mode
        """
        # TOGGLE DARK MODE STATE
        # Switch the dark mode state
        self.is_dark_mode = not self.is_dark_mode

        # APPLY STYLES
        # Apply appropriate styles based on dark mode state
        if self.is_dark_mode:
            # APPLY DARK MODE
            # Set dark background and adjust widget styles
            self.root.configure(bg="#2e2e2e")
            self.style.theme_use('default')
            self.main_frame.configure(style='Dark.TFrame')
            self.title_label.configure(style='Dark.TLabel')
            self.status_label.configure(style='Dark.TLabel')
            self.convert_btn.configure(style='Dark.TButton')
            self.cancel_btn.configure(style='Dark.TButton')
            self.progress.configure(style='Dark.TProgressbar')
            self.dark_mode_btn.configure(style='Dark.TButton')
            self.dark_mode_btn.config(text="Toggle Light Mode")
        else:
            # APPLY LIGHT MODE
            # Revert to default system colors
            self.root.configure(bg="SystemButtonFace")
            self.style.theme_use('default')
            self.main_frame.configure(style='TFrame')
            self.title_label.configure(style='TLabel')
            self.status_label.configure(style='TLabel')
            self.convert_btn.configure(style='TButton')
            self.cancel_btn.configure(style='TButton')
            self.progress.configure(style='TProgressbar')
            self.dark_mode_btn.configure(style='TButton')
            self.dark_mode_btn.config(text="Toggle Dark Mode")

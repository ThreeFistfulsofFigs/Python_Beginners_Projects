# ============================================================================
# MAGIC NOTEPAD APPLICATION
# ============================================================================
# A simple text editor built with Tkinter that provides basic file operations.
# Features include text editing, file saving, and file loading capabilities
# with a clean, user-friendly interface.
# ============================================================================

# Import required libraries
import tkinter as tk  # Core GUI framework
from tkinter import filedialog, Text, Frame, Button  # Specific GUI components


# ============================================================================
# MAIN APPLICATION CLASS
# ============================================================================
class SimpleNotepad:
    """
    A simple notepad application with basic text editing and file operations.

    This class creates a GUI application that allows users to:
    - Edit text in a scrollable text area
    - Save text content to files
    - Load text content from files
    - Basic file management with error handling
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the SimpleNotepad application with GUI components.

        Args:
            root (tk.Tk): The main Tkinter window instance.
        """
        # MAIN WINDOW SETUP
        self.root = root
        self.root.title("Magic Notepad")

        # TEXT AREA CREATION
        # Create main text editing widget with word wrapping
        # expand=True allows widget to grow with window
        # fill="both" makes widget expand in both directions
        self.text_area: Text = Text(self.root, wrap="word")
        self.text_area.pack(expand=True, fill="both")

        # BUTTON CONTAINER SETUP
        # Create frame to organize control buttons
        self.button_frame: Frame = Frame(self.root)
        self.button_frame.pack(expand=True, fill="both")

        # SAVE BUTTON CREATION
        # Button to trigger file saving functionality
        # side=tk.LEFT arranges buttons horizontally
        self.save_button: Button = Button(
            self.button_frame,
            text="Save",
            command=self.save_file
        )
        self.save_button.pack(side=tk.LEFT)

        # LOAD BUTTON CREATION
        # Button to trigger file loading functionality
        self.load_button: Button = Button(
            self.button_frame,
            text="Load",
            command=self.load_file
        )
        self.load_button.pack(side=tk.LEFT)

    # ============================================================================
    # FILE OPERATIONS - SAVE FUNCTIONALITY
    # ============================================================================
    def save_file(self) -> None:
        """
        Saves the current text area content to a user-selected file.

        Opens a file dialog for the user to choose save location and filename.
        Handles user cancellation and file writing errors gracefully.

        Raises:
            IOError: If there is an error writing to the selected file.
        """
        # FILE DIALOG FOR SAVE LOCATION
        # Show save dialog with default .txt extension
        # filetypes limits visible files to text files for user convenience
        file_path: str = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        # HANDLE USER CANCELLATION
        # filedialog returns empty string if user cancels
        if not file_path:
            print("Save canceled by user.")
            return

        # FILE WRITING OPERATION
        try:
            # CONTENT EXTRACTION AND WRITING
            # Get all text from text area (1.0 = line 1, character 0)
            # tk.END represents the end of all text
            # Use UTF-8 encoding to support international characters
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.text_area.get(1.0, tk.END))

            # SUCCESS CONFIRMATION
            print(f"File saved to: {file_path}")

        # ERROR HANDLING
        except IOError as e:
            print(f"Error saving file: {e}")

    # ============================================================================
    # FILE OPERATIONS - LOAD FUNCTIONALITY
    # ============================================================================
    def load_file(self) -> None:
        """
        Loads content from a user-selected file into the text area.

        Opens a file dialog for the user to choose a file to load.
        Clears current text area content and replaces it with file content.
        Handles user cancellation and file reading errors gracefully.

        Raises:
            FileNotFoundError: If the selected file does not exist.
            IOError: If there is an error reading the selected file.
        """
        # FILE DIALOG FOR FILE SELECTION
        # Show open dialog with .txt filter for user convenience
        file_path: str = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        # HANDLE USER CANCELLATION
        # filedialog returns empty string if user cancels
        if not file_path:
            print("Load canceled by user.")
            return

        # FILE READING OPERATION
        try:
            # CONTENT READING
            # Read entire file content with UTF-8 encoding
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            # TEXT AREA UPDATE
            # Clear existing content (delete from start to end)
            self.text_area.delete(1.0, tk.END)

            # INSERT NEW CONTENT
            # tk.INSERT represents current cursor position
            self.text_area.insert(tk.INSERT, content)

            # SUCCESS CONFIRMATION
            print(f"File loaded from: {file_path}")

        # ERROR HANDLING
        # Handle both missing files and general I/O errors
        except (FileNotFoundError, IOError) as e:
            print(f"Error loading file: {e}")

    # ============================================================================
    # APPLICATION LIFECYCLE MANAGEMENT
    # ============================================================================
    def run(self) -> None:
        """
        Starts the Tkinter main event loop to run the application.

        This method begins the GUI event handling and keeps the application
        running until the user closes the window.
        """
        # START GUI EVENT LOOP
        # mainloop() handles all GUI events (clicks, typing, window operations)
        # This call blocks until the application window is closed
        self.root.mainloop()


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================
def main() -> None:
    """
    Main function to initialize and run the Magic Notepad application.

    Creates the main Tkinter window, initializes the SimpleNotepad class,
    and starts the application event loop.
    """
    # MAIN WINDOW CREATION
    # Create the root Tkinter window that will contain all GUI elements
    root: tk.Tk = tk.Tk()

    # APPLICATION INITIALIZATION
    # Create SimpleNotepad instance with the root window
    app: SimpleNotepad = SimpleNotepad(root)

    # APPLICATION EXECUTION
    # Start the application's main event loop
    app.run()


# ============================================================================
# PROGRAM EXECUTION GUARD
# ============================================================================
if __name__ == "__main__":
    # Execute main function only when script is run directly
    # (not when imported as a module)
    main()
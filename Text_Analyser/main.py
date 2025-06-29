# ============================================================================
# WORD FREQUENCY ANALYZER APPLICATION
# ============================================================================
# A text analysis tool built with Tkinter that provides detailed statistics
# for text files, including character, word, sentence, and paragraph counts,
# as well as word frequency analysis. Features a user-friendly GUI with file
# selection, text preview, and result saving capabilities.
# ============================================================================

# Import required libraries
import tkinter as tk                # Core GUI framework
from tkinter import ttk, filedialog, messagebox, scrolledtext  # Specific GUI components
import os                          # File path operations
import re                          # Regular expressions for text analysis
from pathlib import Path           # File path handling
from collections import Counter    # Word frequency counting
from typing import Dict, Union     # Type hints for better code clarity

# ============================================================================
# MAIN APPLICATION CLASS
# ============================================================================
class TextAnalyzerGUI:
    """
    A text analyzer application with a Tkinter GUI for analyzing text files.

    This class creates a GUI application that allows users to:
    - Select and load text files for analysis
    - Preview file content (full or truncated)
    - Analyze text for character, word, sentence, and paragraph statistics
    - View detailed word frequency results
    - Save analysis results to a file
    - Clear the interface for new analysis
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the TextAnalyzerGUI application with GUI components.

        Args:
            root (tk.Tk): The main Tkinter window instance.
        """
        # MAIN WINDOW SETUP
        self.root: tk.Tk = root
        self.root.title("Text Analyzer - Enhanced GUI Version")
        self.root.geometry("900x700")  # Set initial window size
        self.root.minsize(800, 600)    # Set minimum window size for usability

        # INSTANCE VARIABLES
        # Store current file path, text content, and analysis results
        self.current_file_path: tk.StringVar = tk.StringVar()
        self.current_text: str = ""
        self.analysis_results: Dict = {}

        # INITIALIZE GUI
        # Set up the main interface components
        self.setup_gui()

    # ============================================================================
    # GUI SETUP
    # ============================================================================
    def setup_gui(self) -> None:
        """
        Creates and configures the main GUI layout with responsive design.

        Sets up frames, labels, buttons, text areas, and status bar for file
        selection, text preview, analysis controls, and results display.
        """
        # MAIN CONTAINER SETUP
        # Create main frame with padding for layout spacing
        main_frame: ttk.Frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # CONFIGURE GRID WEIGHTS
        # Enable responsive resizing for main window and frame
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)

        # TITLE LABEL
        # Display application title with bold font
        title_label: ttk.Label = ttk.Label(
            main_frame, text="📝 Text Analyzer", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # FILE SELECTION SECTION
        # Create labeled frame for file selection controls
        file_frame: ttk.LabelFrame = ttk.LabelFrame(
            main_frame, text="📁 File Selection", padding="10"
        )
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)

        # FILE SELECTION BUTTONS AND ENTRY
        # Button to browse files and readonly entry for file path
        ttk.Button(file_frame, text="Browse File", command=self.browse_file).grid(
            row=0, column=0, padx=(0, 10)
        )
        self.file_path_entry: ttk.Entry = ttk.Entry(
            file_frame, textvariable=self.current_file_path, state="readonly"
        )
        self.file_path_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(file_frame, text="Analyze", command=self.analyze_file, style="Accent.TButton").grid(
            row=0, column=2
        )

        # TEXT PREVIEW SECTION
        # Create labeled frame for text preview display
        preview_frame: ttk.LabelFrame = ttk.LabelFrame(
            main_frame, text="📖 Text Preview", padding="10"
        )
        preview_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)

        # TEXT PREVIEW WIDGET
        # Scrollable text area for showing file content
        self.text_preview: scrolledtext.ScrolledText = scrolledtext.ScrolledText(
            preview_frame, height=8, wrap=tk.WORD, state=tk.DISABLED
        )
        self.text_preview.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # PREVIEW CONTROL BUTTONS
        # Buttons to toggle between full text and preview
        preview_controls: ttk.Frame = ttk.Frame(preview_frame)
        preview_controls.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        ttk.Button(preview_controls, text="Show Full Text", command=self.show_full_text).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        ttk.Button(preview_controls, text="Show Preview Only", command=self.show_preview_only).pack(
            side=tk.LEFT
        )

        # ANALYSIS CONTROL BUTTONS
        # Frame for analysis and save/clear buttons
        controls_frame: ttk.Frame = ttk.Frame(main_frame)
        controls_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        ttk.Button(controls_frame, text="📊 Detailed Analysis", command=self.show_detailed_analysis).pack(
            side=tk.LEFT, padx=(0, 10)
        )
        ttk.Button(controls_frame, text="💾 Save Results", command=self.save_results).pack(
            side=tk.LEFT, padx=(0, 10)
        )
        ttk.Button(controls_frame, text="🔄 Clear", command=self.clear_all).pack(side=tk.LEFT)

        # RESULTS SECTION
        # Create labeled frame for analysis results display
        results_frame: ttk.LabelFrame = ttk.LabelFrame(
            main_frame, text="📈 Analysis Results", padding="10"
        )
        results_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        # RESULTS TEXT WIDGET
        # Scrollable text area for showing analysis results
        self.results_text: scrolledtext.ScrolledText = scrolledtext.ScrolledText(
            results_frame, height=12, wrap=tk.WORD, state=tk.DISABLED
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # STATUS BAR
        # Display application status and feedback
        self.status_var: tk.StringVar = tk.StringVar(value="Ready to analyze text files...")
        status_bar: ttk.Label = ttk.Label(
            main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W
        )
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))

    # ============================================================================
    # FILE OPERATIONS - FILE SELECTION
    # ============================================================================
    def browse_file(self) -> None:
        """
        Opens a file dialog to select a text file for analysis.

        Supports .txt, .md, and all file types. Updates the file path entry
        and status bar with the selected file's name.
        """
        # FILE TYPE CONFIGURATION
        # Define supported file types for dialog
        file_types: list = [
            ("Text files", "*.txt"),
            ("Markdown files", "*.md"),
            ("All files", "*.*")
        ]

        # FILE DIALOG
        # Open dialog for selecting a file
        filename: str = filedialog.askopenfilename(
            title="Select a text file to analyze",
            filetypes=file_types
        )

        # UPDATE FILE PATH
        # Set file path and update status if file selected
        if filename:
            self.current_file_path.set(filename)
            self.status_var.set(f"Selected: {os.path.basename(filename)}")

    # ============================================================================
    # FILE OPERATIONS - FILE READING
    # ============================================================================
    def open_file(self, path: str) -> str:
        """
        Opens and reads a text file with multiple encoding fallbacks.

        Attempts to read the file with UTF-8 encoding, falling back to other
        encodings if necessary. Handles file not found and general errors.

        Args:
            path (str): The file path to read.

        Returns:
            str: The file content or an error message if reading fails.

        Raises:
            UnicodeDecodeError: If the file cannot be decoded.
            FileNotFoundError: If the file does not exist.
            Exception: For other unexpected errors.
        """
        # FILE READING ATTEMPT WITH UTF-8
        try:
            with open(path, "r", encoding="utf-8") as file:
                return file.read()

        # HANDLE ENCODING ERRORS
        except UnicodeDecodeError:
            # Try fallback encodings for compatibility
            encodings: list = ["latin-1", "cp1252", "iso-8859-1"]
            for encoding in encodings:
                try:
                    with open(path, "r", encoding=encoding) as file:
                        return file.read()
                except UnicodeDecodeError:
                    continue
            return f"Could not decode file '{path}' with any common encoding."

        # HANDLE FILE NOT FOUND
        except FileNotFoundError:
            return f"File {path} not found."

        # HANDLE OTHER ERRORS
        except Exception as e:
            return f"Something went wrong ({e})!"

    # ============================================================================
    # TEXT ANALYSIS FUNCTIONALITY
    # ============================================================================
    def analyze_text(self, text: str) -> Dict[str, Union[int, float, Dict[str, int]]]:
        """
        Performs comprehensive text analysis on the provided text.

        Analyzes character counts, word counts, sentence counts, paragraph counts,
        and word frequency. Returns a dictionary with statistics and top 10 words.

        Args:
            text (str): The text to analyze.

        Returns:
            Dict[str, Union[int, float, Dict[str, int]]]: Analysis results or error message.
        """
        # CHECK FOR ERROR MESSAGES
        # Return early if text contains error from file reading
        if text.startswith(("Could not decode", "File", "Something went wrong")):
            return {"error": text}

        # CHARACTER ANALYSIS
        # Count total characters, spaces, and non-space characters
        total_chars: int = len(text)
        total_chars_no_spaces: int = len(text.replace(" ", ""))
        total_spaces: int = text.count(" ")

        # WORD ANALYSIS
        # Split text into words and count
        words: list = text.split()
        total_words: int = len(words)

        # SENTENCE ANALYSIS
        # Split by sentence-ending punctuation and filter valid sentences
        sentences: list = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        total_sentences: int = len(sentences)

        # PARAGRAPH ANALYSIS
        # Split by double newlines and filter valid paragraphs
        paragraphs: list = [p.strip() for p in text.split('\n\n') if p.strip()]
        total_paragraphs: int = len(paragraphs)

        # LINE ANALYSIS
        # Count lines by splitting on newlines
        lines: list = text.split('\n')
        total_lines: int = len(lines)

        # AVERAGE CALCULATIONS
        # Compute average words per sentence and characters per word
        avg_words_per_sentence: float = total_words / total_sentences if total_sentences > 0 else 0
        avg_chars_per_word: float = total_chars_no_spaces / total_words if total_words > 0 else 0

        # WORD FREQUENCY ANALYSIS
        # Count word occurrences, ignoring case and punctuation
        word_freq: Counter = Counter(word.lower().strip('.,!?";:()[]{}') for word in words)
        top_words: Dict[str, int] = dict(word_freq.most_common(10))

        # UNIQUE WORDS
        # Count unique words, ignoring case and punctuation
        unique_words: int = len(set(word.lower().strip('.,!?";:()[]{}') for word in words))

        # RETURN RESULTS
        return {
            "total_characters": total_chars,
            "total_characters_no_spaces": total_chars_no_spaces,
            "total_spaces": total_spaces,
            "total_words": total_words,
            "unique_words": unique_words,
            "total_sentences": total_sentences,
            "total_paragraphs": total_paragraphs,
            "total_lines": total_lines,
            "avg_words_per_sentence": round(avg_words_per_sentence, 2),
            "avg_characters_per_word": round(avg_chars_per_word, 2),
            "top_10_words": top_words
        }

    # ============================================================================
    # FILE ANALYSIS
    # ============================================================================
    def analyze_file(self) -> None:
        """
        Analyzes the selected file and displays results.

        Reads the file, performs text analysis, and updates the GUI with a preview
        and basic statistics. Handles errors with user feedback.
        """
        # CHECK FOR FILE SELECTION
        # Ensure a file is selected before proceeding
        if not self.current_file_path.get():
            messagebox.showwarning("No File Selected", "Please select a file to analyze.")
            return

        # UPDATE STATUS
        # Indicate file processing
        self.status_var.set("Reading and analyzing file...")
        self.root.update()

        # READ FILE
        # Load file content using open_file method
        self.current_text = self.open_file(self.current_file_path.get())

        # CHECK FOR FILE ERRORS
        # Display error if file reading failed
        if self.current_text.startswith(("Could not decode", "File", "Something went wrong")):
            messagebox.showerror("File Error", self.current_text)
            self.status_var.set("Error reading file")
            return

        # DISPLAY PREVIEW
        # Show truncated text preview
        self.show_preview_only()

        # PERFORM ANALYSIS
        # Analyze text and store results
        self.analysis_results = self.analyze_text(self.current_text)

        # CHECK FOR ANALYSIS ERRORS
        # Display error if analysis failed
        if "error" in self.analysis_results:
            messagebox.showerror("Analysis Error", self.analysis_results["error"])
            return

        # DISPLAY RESULTS
        # Show basic statistics in GUI
        self.display_basic_results()
        self.status_var.set("Analysis complete!")

    # ============================================================================
    # TEXT PREVIEW - SHOW PREVIEW
    # ============================================================================
    def show_preview_only(self) -> None:
        """
        Displays a preview of the text (first 500 characters) in the text area.

        Truncates long text and adds a note for user to view full text.
        """
        # CHECK FOR TEXT
        # Return if no text is loaded
        if not self.current_text:
            return

        # PREPARE PREVIEW
        # Take first 500 characters and indicate truncation
        preview: str = self.current_text[:500]
        if len(self.current_text) > 500:
            preview += "\n\n... (text truncated - click 'Show Full Text' to see all)"

        # UPDATE TEXT AREA
        # Clear and insert preview text
        self.text_preview.config(state=tk.NORMAL)
        self.text_preview.delete(1.0, tk.END)
        self.text_preview.insert(1.0, preview)
        self.text_preview.config(state=tk.DISABLED)

    # ============================================================================
    # TEXT PREVIEW - SHOW FULL TEXT
    # ============================================================================
    def show_full_text(self) -> None:
        """
        Displays the complete text content in the text area.
        """
        # CHECK FOR TEXT
        # Return if no text is loaded
        if not self.current_text:
            return

        # UPDATE TEXT AREA
        # Clear and insert full text
        self.text_preview.config(state=tk.NORMAL)
        self.text_preview.delete(1.0, tk.END)
        self.text_preview.insert(1.0, self.current_text)
        self.text_preview.config(state=tk.DISABLED)

    # ============================================================================
    # RESULTS DISPLAY - BASIC STATISTICS
    # ============================================================================
    def display_basic_results(self) -> None:
        """
        Displays basic analysis results in the GUI results text area.

        Shows character, word, sentence, paragraph counts, and averages.
        """
        # CHECK FOR RESULTS
        # Return if no analysis results exist
        if not self.analysis_results:
            return

        # FORMAT RESULTS
        # Prepare text for basic statistics display
        results_text: str = "📊 BASIC STATISTICS:\n"
        results_text += "─" * 50 + "\n"
        results_text += f"Total characters (with spaces):    {self.analysis_results['total_characters']:,}\n"
        results_text += f"Total characters (without spaces): {self.analysis_results['total_characters_no_spaces']:,}\n"
        results_text += f"Total spaces:                      {self.analysis_results['total_spaces']:,}\n"
        results_text += f"Total words:                       {self.analysis_results['total_words']:,}\n"
        results_text += f"Unique words:                      {self.analysis_results['unique_words']:,}\n"
        results_text += f"Total sentences:                   {self.analysis_results['total_sentences']:,}\n"
        results_text += f"Total paragraphs:                  {self.analysis_results['total_paragraphs']:,}\n"
        results_text += f"Total lines:                       {self.analysis_results['total_lines']:,}\n\n"
        results_text += "📈 AVERAGES:\n"
        results_text += "─" * 20 + "\n"
        results_text += f"Average words per sentence:        {self.analysis_results['avg_words_per_sentence']}\n"
        results_text += f"Average characters per word:       {self.analysis_results['avg_characters_per_word']}\n"

        # UPDATE RESULTS TEXT AREA
        # Clear and insert formatted results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results_text)
        self.results_text.config(state=tk.DISABLED)

    # ============================================================================
    # RESULTS DISPLAY - DETAILED ANALYSIS
    # ============================================================================
    def show_detailed_analysis(self) -> None:
        """
        Displays detailed analysis results, including word frequency, in a new window.
        """
        # CHECK FOR RESULTS
        # Prompt user if no analysis results exist
        if not self.analysis_results:
            messagebox.showinfo("No Analysis", "Please analyze a file first.")
            return

        # CREATE NEW WINDOW
        # Set up a new window for detailed results
        detail_window: tk.Toplevel = tk.Toplevel(self.root)
        detail_window.title("Detailed Analysis Results")
        detail_window.geometry("600x500")

        # CREATE TEXT WIDGET
        # Scrollable text area for detailed results
        detail_text: scrolledtext.ScrolledText = scrolledtext.ScrolledText(
            detail_window, wrap=tk.WORD, padx=10, pady=10
        )
        detail_text.pack(fill=tk.BOTH, expand=True)

        # FORMAT DETAILED RESULTS
        # Prepare text for detailed statistics and word frequency
        detailed_results: str = "🔍 DETAILED TEXT ANALYSIS RESULTS\n"
        detailed_results += "═" * 60 + "\n\n"
        detailed_results += "📊 BASIC STATISTICS:\n"
        detailed_results += "─" * 25 + "\n"
        for key, value in self.analysis_results.items():
            if key != 'top_10_words':
                formatted_key: str = key.replace('_', ' ').title()
                detailed_results += f"{formatted_key:<30}: {value:>10}\n"
        detailed_results += "\n🔤 TOP 10 MOST COMMON WORDS:\n"
        detailed_results += "─" * 35 + "\n"
        for word, count in self.analysis_results['top_10_words'].items():
            detailed_results += f"{word:<20} : {count:>3} times\n"

        # INSERT RESULTS
        # Display detailed results in new window
        detail_text.insert(1.0, detailed_results)
        detail_text.config(state=tk.DISABLED)

    # ============================================================================
    # FILE OPERATIONS - SAVE RESULTS
    # ============================================================================
    def save_results(self) -> None:
        """
        Saves analysis results to a user-selected file.

        Opens a file dialog for choosing save location and filename.
        Saves results in a formatted text file.

        Raises:
            Exception: If there is an error writing to the file.
        """
        # CHECK FOR RESULTS
        # Prompt user if no analysis results exist
        if not self.analysis_results:
            messagebox.showinfo("No Results", "Please analyze a file first.")
            return

        # FILE DIALOG FOR SAVE LOCATION
        # Open dialog for saving results
        filename: str = filedialog.asksaveasfilename(
            title="Save Analysis Results",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        # HANDLE USER CANCELLATION
        # filedialog returns empty string if user cancels
        if filename:
            try:
                # WRITE RESULTS TO FILE
                # Save formatted results with file path
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("TEXT ANALYSIS RESULTS\n")
                    f.write("=" * 50 + "\n")
                    f.write(f"File analyzed: {self.current_file_path.get()}\n\n")
                    for key, value in self.analysis_results.items():
                        if key != 'top_10_words':
                            f.write(f"{key}: {value}\n")
                        else:
                            f.write(f"\nTop 10 most common words:\n")
                            for word, count in value.items():
                                f.write(f"  {word}: {count}\n")

                # SUCCESS FEEDBACK
                messagebox.showinfo("Success", f"Results saved to {filename}")
                self.status_var.set(f"Results saved to {os.path.basename(filename)}")

            # ERROR HANDLING
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save file: {e}")

    # ============================================================================
    # INTERFACE RESET
    # ============================================================================
    def clear_all(self) -> None:
        """
        Clears all data and resets the GUI to its initial state.

        Resets file path, text content, analysis results, and text areas.
        """
        # RESET VARIABLES
        # Clear stored data
        self.current_file_path.set("")
        self.current_text = ""
        self.analysis_results = {}

        # CLEAR TEXT PREVIEW
        # Reset text preview area
        self.text_preview.config(state=tk.NORMAL)
        self.text_preview.delete(1.0, tk.END)
        self.text_preview.config(state=tk.DISABLED)

        # CLEAR RESULTS
        # Reset results text area
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)

        # UPDATE STATUS
        # Reset status bar message
        self.status_var.set("Ready to analyze text files...")

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================
def main() -> None:
    """
    Main function to initialize and run the Text Analyzer application.

    Creates the main Tkinter window, applies a modern theme if available,
    and starts the application event loop.
    """
    # MAIN WINDOW CREATION
    # Create the root Tkinter window
    root: tk.Tk = tk.Tk()

    # THEME SETUP
    # Attempt to apply modern 'clam' theme
    try:
        style: ttk.Style = ttk.Style()
        style.theme_use('clam')  # More modern looking theme
    except:
        pass  # Use default theme if clam is unavailable

    # APPLICATION INITIALIZATION
    # Create TextAnalyzerGUI instance
    app: TextAnalyzerGUI = TextAnalyzerGUI(root)

    # APPLICATION EXECUTION
    # Start the Tkinter main event loop
    root.mainloop()

# ============================================================================
# PROGRAM EXECUTION GUARD
# ============================================================================
if __name__ == "__main__":
    # Execute main function only when script is run directly
    # (not when imported as a module)
    main()

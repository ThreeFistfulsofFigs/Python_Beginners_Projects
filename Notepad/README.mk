Magic Notepad Application
A simple text editor built with Tkinter that provides basic file operations, including text editing, saving, and loading. It features a clean, user-friendly interface suitable for basic note-taking or text file management.
Features

Edit text in a scrollable, word-wrapped text area.
Save text content to files with a user-selected location and filename.
Load text content from existing files into the editor.
Handles file operations with UTF-8 encoding for international character support.
Includes basic error handling for file I/O operations.

Technologies Used

Python 3.x
Tkinter (included with Python) for GUI

Requirements

Python 3.x installed

Installation

Clone or copy the main.py script to your project directory.
No additional packages are required.

Usage

Run the script:python main.py


A window titled "Magic Notepad" will open with a text area and two buttons ("Save" and "Load").
Type or edit text in the text area.
Click "Save" to save the content:
Select a file location and name via the dialog (defaults to .txt).
Canceling the dialog exits without saving.


Click "Load" to open a file:
Select a .txt file via the dialog to load its content.
Canceling the dialog exits without loading.


Close the window to exit the application.

Notes

Saved and loaded files use UTF-8 encoding for broad character support.
Console messages confirm save/load actions or report errors (e.g., file not found).
The interface is basic and does not include advanced features like undo/redo.

Limitations

No persistent state (e.g., unsaved changes are lost on exit).
No formatting options (plain text only).
File type is restricted to .txt via the dialog filter.

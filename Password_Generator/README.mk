Password Generator
A Python-based tool that generates cryptographically secure passwords with customizable length and character types. It includes validation to ensure required character types are present and evaluates password strength based on complexity criteria, making it ideal for creating strong, secure passwords.
Features

Generates passwords using cryptographically secure random selection.
Customizable length (default: 12) and character types (uppercase letters, symbols).
Validates that passwords include required character types (e.g., uppercase or symbols).
Evaluates password strength with a score (0-100) and descriptive rating (Very Weak to Very Strong).
Generates and displays 10 passwords by default with their strength assessments.

Technologies Used

Python 3.x
secrets (included with Python) for secure random generation
string (included with Python) for character sets
re (included with Python) for regular expression validation

Requirements

Python 3.x installed

Installation

Clone or copy the main.py script to your project directory.
No additional packages are required.

Usage

Run the script:python main.py


The script will generate and display 10 passwords, each with its length, strength rating, and score.
To customize password generation (e.g., length, uppercase, symbols), modify the Password class instantiation in the main function (e.g., Password(length=16, uppercase=False, symbols=True)).

Notes

Default settings generate 20-character passwords with uppercase letters and symbols.
Strength is scored based on length (up to 30 points), character types (up to 60 points), and complexity bonus (up to 10 points).
Output is printed to the console with a separator for readability.

Limitations

No GUI or interactive input for customization (requires code modification).
Generates a fixed number (10) of passwords per run.
No persistent storage for generated passwords.

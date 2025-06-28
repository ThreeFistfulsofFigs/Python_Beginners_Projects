# Password Generator

## Overview
The Password Generator is a Python command-line tool that creates cryptographically secure passwords with customizable length and character types. It validates passwords for required characters and evaluates strength based on complexity criteria.

## Features
- **Secure Generation**: Uses `secrets` for cryptographically secure passwords.
- **Customizable Options**: Set length and include/exclude uppercase letters and symbols.
- **Strength Evaluation**: Scores passwords based on length and character diversity.
- **Validation**: Ensures passwords meet specified character requirements.
- **Console Output**: Displays multiple passwords with strength scores.

## Requirements
- **Operating System**: Any (Windows, macOS, Linux)
- **Python**: 3.7 or higher
- **Dependencies**: Built-in `secrets`, `string`, `re` modules

## Installation

### Step 1: Set Up Environment
1. **Install Python**: Ensure Python 3.7+ is installed and added to PATH.
   ```bash
   python --version
   ```
2. **Create Virtual Environment** (optional but recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

### Step 2: Run the Script
1. **Locate Script**: Navigate to the project directory containing `main.py`.
2. **Run the Script**:
   ```bash
   python main.py
   ```

## Usage

### Step 1: Generate Passwords
1. **Run the Script**: Generates 10 passwords with default settings (20 characters, uppercase, symbols).
2. **View Results**:
   - Output shows passwords and strength (e.g., `Password: X7$k9mPq... Strength: Very Strong (Score: 85/100)`).

### Step 2: Customize Settings
1. **Modify Parameters**: Edit `main.py` to change `length`, `uppercase`, or `symbols` in `Password` initialization.
   ```python
   password_generator = Password(length=16, uppercase=True, symbols=False)
   ```
2. **Test Variations**:
   - Run with different settings and verify passwords meet criteria (e.g., no symbols if `symbols=False`).

### Step 3: Testing
1. **Test Password Strength**:
   - Verify scores reflect length and character types (e.g., longer passwords score higher).
2. **Test Validation**:
   - Set `uppercase=True` and confirm passwords include uppercase letters.
   - Check console output for consistent results.

## Configuration
- **Default Settings** (in `main.py`):
  ```python
  length=20
  uppercase=True
  symbols=True
  ```

## Troubleshooting

### Weak Passwords Generated
- Increase `length` or enable `uppercase`/`symbols` in `main.py`.
- Verify `secrets` module is used (not `random`).

### No Output
- Ensure Python 3.7+ is installed: `python --version`.
- Check for syntax errors in `main.py`.

## Files Included
- `main.py`: Core script with password generation and strength evaluation.

## Notes
- **Version**: 1.0.0
- **Security**: Uses `secrets` for cryptographic security; avoid using `random` module.

## Support
For issues, check console output or submit an issue at [GitHub repository URL] (replace with your repo URL).
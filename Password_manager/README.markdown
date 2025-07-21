# Password Manager Pro

## Overview
Password Manager Pro is a secure password management application built with Python and a modern Tkinter GUI using `ttkbootstrap`. It allows users to generate, store, view, edit, and delete passwords securely with AES-256 encryption, protected by a master password. The application supports password generation with customizable options, import/export functionality, and a user-friendly interface with theme switching.

## Features
- **Secure Storage**: Uses AES-256 encryption with Fernet and PBKDF2 key derivation for secure password storage.
- **Master Password Authentication**: Requires a master password on startup, verified by decrypting a test string, with a limit of 3 failed attempts.
- **Password Management**: Add, view, edit, delete, and search passwords via a tabbed GUI.
- **Password Generation**: Generate strong, customizable passwords with options for length and character types (uppercase, lowercase, numbers, symbols).
- **Import/Export**: Export passwords as decrypted JSON or import from JSON files, with duplicate handling.
- **Modern UI**: Features a responsive GUI with theme switching (superhero, darkly, cyborg, vapor) and context menus.
- **Local Storage**: Stores encrypted passwords in `passwords.json` and configuration in `config.json`.

## Tech Stack
- Python 3.7+
- `tkinter` (standard library, for GUI)
- `ttkbootstrap>=1.10.1` (for modern GUI styling)
- `cryptography>=36.0.0` (for AES-256 encryption and key derivation)
- Standard libraries: `json`, `os`, `datetime`, `secrets`, `base64`

## Setup
1. **Install Python**: Ensure Python 3.7 or higher is installed and added to PATH.
   ```bash
   python --version
   ```
2. **Set Up Virtual Environment** (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```
3. **Install Dependencies**:
   ```bash
   pip install ttkbootstrap cryptography
   ```
4. **Linux Only**: Ensure `tkinter` is installed for GUI support:
   ```bash
   sudo apt-get install python3-tk
   ```

## Usage
1. Navigate to the project directory:
   ```bash
   cd password_manager
   ```
2. Run the application:
   ```bash
   python main.py
   ```
3. **First Run**: Set a master password when prompted.
4. **Subsequent Runs**: Enter the master password (3 attempts allowed). The app will exit on failure or cancellation.
5. **GUI Navigation**:
   - **Add Password Tab**: Enter website, email/username, and password (or generate one), then click "Save" or press `Ctrl+S`.
   - **View Passwords Tab**: Search passwords, right-click for context menu (copy, edit, delete), or double-click to copy passwords.
   - **Settings Tab**: Adjust password generation settings, change the master password, or import/export passwords.
6. **Shortcuts**:
   - `Ctrl+G`: Generate password
   - `Ctrl+S`: Save password
7. **Data Storage**: Passwords are stored in `passwords.json`, and configuration (including salt and test string) is stored in `config.json`.

## Troubleshooting
- **GUI Not Displaying**: Ensure `tkinter` and `ttkbootstrap` are installed (`pip install ttkbootstrap` and `sudo apt-get install python3-tk` on Linux).
- **Authentication Errors**: Verify the correct master password. After 3 failed attempts, the app exits. Check `config.json` for valid `salt` and `test_string`.
- **File Errors**: Ensure write permissions for `passwords.json` and `config.json`. Verify files are not corrupted.
- **Decryption Errors**: If passwords fail to decrypt, confirm the master password or check `passwords.json` for corruption.
- **Module Not Found**: Install missing dependencies (`pip install ttkbootstrap cryptography`).
- **Theme Issues**: Ensure `ttkbootstrap` themes are available; reinstall if themes fail to load.

## Notes
- **Security**: The master password is not stored; a salt and encrypted test string are saved in `config.json`. Keep `config.json` and `passwords.json` secure.
- **Exporting Passwords**: Exported passwords are decrypted in the JSON file; store the exported file securely.
- **Executable**: Can be converted to a standalone executable using PyInstaller:
  ```bash
  pip install pyinstaller
  pyinstaller --onefile main.py
  ```
- **Directory**: `password_manager`
- **License**: MIT (see repository's LICENSE file).
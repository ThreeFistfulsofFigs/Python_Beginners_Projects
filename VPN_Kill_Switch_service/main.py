# ============================================================================
# VPN KILL SWITCH BUILD SETUP UTILITY
# ============================================================================
# Script to generate build-related files for the VPN Kill Switch application.
# Creates setup.py, manifest.xml, requirements.txt, build.bat, installer.py,
# and README.md for building and installing the executable.
# ============================================================================

# IMPORT REQUIRED LIBRARIES
import os  # Operating system interfaces
import sys  # System utilities
import subprocess  # Subprocess execution
from pathlib import Path  # Filesystem path operations


# ============================================================================
# SETUP FILE GENERATION
# ============================================================================
def create_setup_files() -> None:
    """
    Create all necessary setup files for building the VPN Kill Switch executable.

    Generates:
    - setup.py: PyInstaller configuration
    - manifest.xml: Windows UAC manifest for admin privileges
    - requirements.txt: Project dependencies
    - build.bat: Automated build script
    - installer.py: System installer for shortcuts and registry
    - README.md: Project documentation and deployment instructions
    """
    # SETUP.PY CONTENT
    # Define PyInstaller configuration for building the executable
    setup_py_content: str = '''
# ============================================================================
# PYINSTALLER BUILD CONFIGURATION
# ============================================================================
# Script to build the VPN Kill Switch application into a single executable.
# Configures PyInstaller to package the application with required dependencies.
# ============================================================================

# IMPORT REQUIRED LIBRARIES
import PyInstaller.__main__  # PyInstaller build interface
import sys  # System utilities
import os  # Operating system interfaces


# ============================================================================
# BUILD EXECUTABLE FUNCTION
# ============================================================================
def build_executable() -> None:
    """
    Build the executable using PyInstaller.

    Configures PyInstaller with options to create a single executable file,
    including dependencies and manifest file, with admin privileges.
    """
    # PYINSTALLER ARGUMENT SETUP
    args: list[str] = [
        'vpn_killswitch_gui.py',          # Main script
        '--onefile',                      # Single executable file
        '--windowed',                     # No console window
        '--name=VPN_KillSwitch_Config',   # Executable name
        '--add-data=manifest.xml;.',      # Include manifest
        '--hidden-import=tkinter',        # Ensure tkinter is included
        '--hidden-import=psutil',         # Ensure psutil is included
        '--hidden-import=win32com',       # Ensure pywin32 is included
        '--clean',                        # Clean build
        '--noconfirm',                    # Overwrite without confirmation
        '--uac-admin',                    # Request admin privileges
    ]

    # BUILD EXECUTION
    print("Building executable with PyInstaller...")
    PyInstaller.__main__.run(args)
    print("Build complete! Check the 'dist' folder for the executable.")

# ============================================================================
# PROGRAM EXECUTION GUARD
# ============================================================================
if __name__ == "__main__":
    # Execute build function only when script is run directly
    build_executable()
'''

    # MANIFEST.XML CONTENT
    # Define Windows UAC manifest for admin privileges
    manifest_content: str = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="1.0.0.0"
    processorArchitecture="*"
    name="VPN_KillSwitch_Config"
    type="win32"
  />
  <description>VPN Kill Switch Configuration Tool</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1">
    <application>
      <supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"/>
      <supportedOS Id="{1f676c76-80e1-4239-95bb-83d0f6d0da78}"/>
      <supportedOS Id="{4a2f28e3-53b9-4441-ba9c-d69d4a4a6e38}"/>
      <supportedOS Id="{35138b9a-5d96-4fbd-8e2d-a2440225f93a}"/>
      <supportedOS Id="{e2011457-1546-43c5-a5fe-008deee3d3f0}"/>
    </application>
  </compatibility>
</assembly>'''

    # REQUIREMENTS.TXT CONTENT
    # List project dependencies
    requirements_content: str = '''# ============================================================================
# REQUIREMENTS FOR VPN KILL SWITCH CONFIGURATION TOOL
# ============================================================================
tkinter
psutil>=5.8.0
PyInstaller>=4.0
pywin32>=306
'''

    # BUILD.BAT CONTENT
    # Define batch script for automated build
    build_script_content: str = '''@echo off
REM ============================================================================
REM BUILD SCRIPT FOR VPN KILL SWITCH EXECUTABLE
REM ============================================================================
REM This batch file automates the build process
REM Run as Administrator for best results
REM ============================================================================

echo Building VPN Kill Switch Configuration Tool...
echo.

REM CHECK PYTHON INSTALLATION
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM CHECK PIP AVAILABILITY
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please ensure pip is installed and try again
    pause
    exit /b 1
)

REM INSTALL DEPENDENCIES
echo Installing required packages...
pip install -r requirements.txt

REM CHECK PYINSTALLER INSTALLATION
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: PyInstaller installation failed
    pause
    exit /b 1
)

REM BUILD EXECUTABLE
echo.
echo Building executable...
python setup.py

REM CHECK BUILD SUCCESS
if exist "dist\\VPN_KillSwitch_Config.exe" (
    echo.
    echo SUCCESS: Executable created successfully!
    echo Location: dist\\VPN_KillSwitch_Config.exe
    echo.
    echo The executable requires administrator privileges to run properly.
    echo Right-click the executable and select "Run as administrator"
    echo.
) else (
    echo.
    echo ERROR: Build failed - executable not found
    echo Check the console output above for errors
    echo.
)

pause
'''

    # INSTALLER.PY CONTENT
    # Define installer script for system-wide installation
    installer_script_content: str = '''# ============================================================================
# VPN KILL SWITCH INSTALLER
# ============================================================================
# Script to install the VPN Kill Switch application system-wide.
# Creates shortcuts and registers the application in Windows.
# ============================================================================

# IMPORT REQUIRED LIBRARIES
import os  # Operating system interfaces
import sys  # System utilities
import shutil  # File operations
import winreg  # Windows registry access
from pathlib import Path  # Filesystem path operations
import tkinter as tk  # GUI framework for dialogs
from tkinter import messagebox, filedialog  # GUI components


# ============================================================================
# INSTALLER CLASS
# ============================================================================
class VPNKillSwitchInstaller:
    """
    Installer for the VPN Kill Switch Configuration Tool.

    Manages installation, shortcut creation, and Windows registry updates.
    """

    def __init__(self) -> None:
        """
        Initialize the installer with application details.
        """
        # APPLICATION SETTINGS
        self.app_name: str = "VPN Kill Switch"
        self.exe_name: str = "VPN_KillSwitch_Config.exe"
        self.default_install_path: Path = Path("C:/Program Files") / self.app_name

    # ============================================================================
    # INSTALLATION PROCESS
    # ============================================================================
    def install(self, install_path: Path | None = None) -> bool:
        """
        Install the application to the specified or default path.

        Args:
            install_path (Path | None): Installation directory, defaults to C:/Program Files.

        Returns:
            bool: True if installation is successful, False otherwise.

        Raises:
            Exception: If there is an error during installation.
        """
        # INSTALLATION SETUP
        try:
            if not install_path:
                install_path = self.default_install_path

            # CREATE INSTALLATION DIRECTORY
            install_path.mkdir(parents=True, exist_ok=True)

            # COPY EXECUTABLE
            exe_source: Path = Path("dist") / self.exe_name
            exe_dest: Path = install_path / self.exe_name

            if exe_source.exists():
                shutil.copy2(exe_source, exe_dest)
                print(f"Installed to: {exe_dest}")

                # CREATE SHORTCUTS
                self.create_desktop_shortcut(exe_dest)
                self.create_start_menu_shortcut(exe_dest)

                # REGISTER PROGRAM
                self.register_program(install_path)

                return True
            else:
                print(f"ERROR: {exe_source} not found!")
                return False

        except Exception as e:
            print(f"Installation failed: {e}")
            return False

    # ============================================================================
    # SHORTCUT CREATION - DESKTOP
    # ============================================================================
    def create_desktop_shortcut(self, exe_path: Path) -> None:
        """
        Create a desktop shortcut for the application.

        Args:
            exe_path (Path): Path to the executable.

        Raises:
            ImportError: If pywin32 is not available.
            Exception: If there is an error creating the shortcut.
        """
        # DESKTOP SHORTCUT CREATION
        try:
            import win32com.client

            desktop: Path = Path.home() / "Desktop"
            shortcut_path: Path = desktop / f"{self.app_name}.lnk"

            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(exe_path)
            shortcut.WorkingDirectory = str(exe_path.parent)
            shortcut.Description = "VPN Kill Switch Configuration Tool"
            shortcut.save()

            print(f"Desktop shortcut created: {shortcut_path}")

        except ImportError:
            print("pywin32 not available - skipping desktop shortcut")
        except Exception as e:
            print(f"Failed to create desktop shortcut: {e}")

    # ============================================================================
    # SHORTCUT CREATION - START MENU
    # ============================================================================
    def create_start_menu_shortcut(self, exe_path: Path) -> None:
        """
        Create a start menu shortcut for the application.

        Args:
            exe_path (Path): Path to the executable.

        Raises:
            ImportError: If pywin32 is not available.
            Exception: If there is an error creating the shortcut.
        """
        # START MENU SHORTCUT CREATION
        try:
            import win32com.client

            start_menu: Path = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
            app_folder: Path = start_menu / self.app_name
            app_folder.mkdir(exist_ok=True)

            shortcut_path: Path = app_folder / f"{self.app_name}.lnk"

            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(exe_path)
            shortcut.WorkingDirectory = str(exe_path.parent)
            shortcut.Description = "VPN Kill Switch Configuration Tool"
            shortcut.save()

            print(f"Start menu shortcut created: {shortcut_path}")

        except ImportError:
            print("pywin32 not available - skipping start menu shortcut")
        except Exception as e:
            print(f"Failed to create start menu shortcut: {e}")

    # ============================================================================
    # PROGRAM REGISTRATION
    # ============================================================================
    def register_program(self, install_path: Path) -> None:
        """
        Register the program in Windows Add/Remove Programs.

        Args:
            install_path (Path): Installation directory.

        Raises:
            Exception: If there is an error accessing the Windows registry.
        """
        # REGISTRY UPDATE
        try:
            key_path: str = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\" + self.app_name

            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, self.app_name)
                winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, "1.0.0")
                winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, "VPN Kill Switch")
                winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, str(install_path))
                winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, str(install_path / self.exe_name))
                winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, f'"{install_path / self.exe_name}" --uninstall')
                winreg.SetValueEx(key, "NoModify", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "NoRepair", 0, winreg.REG_DWORD, 1)

            print("Program registered in Add/Remove Programs")

        except Exception as e:
            print(f"Failed to register program: {e}")

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================
def main() -> None:
    """
    Main function to run the setup file creation process.

    Initializes the installer and generates all setup files.
    """
    # SETUP FILE CREATION
    create_setup_files()


# ============================================================================
# PROGRAM EXECUTION GUARD
# ============================================================================
if __name__ == "__main__":
    # Execute main function only when script is run directly
    main()
'''

    # README.MD CONTENT
    # Define project documentation with deployment instructions
    readme_content: str = '''# VPN Kill Switch Configuration Tool

## Overview
The VPN Kill Switch Configuration Tool is a Windows application that ensures your internet connection is disabled when your VPN is not active, preventing unprotected network access. It provides a graphical interface for configuring VPN processes, monitoring network status, and managing the kill switch service.

## Features
- **Configuration**: Set VPN processes (e.g., `surfshark.exe`), network interface, and monitoring intervals.
- **Real-Time Monitoring**: Displays service, VPN, and network status.
- **Kill Switch**: Automatically disables the network when no VPN processes are detected.
- **Logging**: Logs events to `%USERPROFILE%\\vpn_killswitch.log` for debugging.
- **Installation**: Installs to `C:\\Program Files\\VPN Kill Switch` with desktop and start menu shortcuts.
- **Windows Integration**: Registers in Add/Remove Programs and supports system startup.

## Requirements
- **Operating System**: Windows 10 or higher
- **Python**: 3.7 or higher (for development/build)
- **Dependencies**:
  - `tkinter` (included with Python)
  - `psutil>=5.8.0`
  - `PyInstaller>=4.0` (for building)
  - `pywin32>=306` (for installation features)

## Building the Executable

### Step 1: Set Up Environment
1. **Install Python**: Ensure Python 3.7+ is installed and added to PATH.
   ```bash
   python --version
   ```
2. **Create Virtual Environment** (optional but recommended):
   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Build the Executable
1. **Option 1: Use `build.bat`** (recommended):
   ```bash
   build.bat
   ```
   Run as administrator to ensure proper dependency installation and build.
2. **Option 2: Use `setup.py`**:
   ```bash
   python setup.py
   ```
3. **Option 3: Use PyInstaller Directly**:
   ```bash
   pyinstaller VPN_KillSwitch_Config.spec
   ```
4. **Output**: The executable `VPN_KillSwitch_Config.exe` will be created in the `dist` folder.

### Step 3: Regenerate Build Files (Optional)
If you modify dependencies or build settings, regenerate build files using `main.py`:
```bash
python main.py
```
This updates `setup.py`, `manifest.xml`, `requirements.txt`, `build.bat`, `installer.py`, and `README.md`.

## Deployment

### Step 1: Run the Executable
1. **Locate Executable**: Find `dist\\VPN_KillSwitch_Config.exe`.
2. **Run as Administrator**: Right-click and select **Run as administrator** (required for network control and installation).
3. **Verify Functionality**:
   - **Configuration Tab**: Set VPN processes (e.g., `surfshark.exe`), network interface (check with `netsh interface show interface`), and save.
   - **Status Tab**: Confirm service, VPN, and network status updates.
   - **Service Management Tab**: Start/stop the kill switch, test network block, or install to startup.

### Step 2: Install System-Wide
1. **Option 1: Use GUI**:
   - In the **Service Management** tab, click **Install to Startup**.
   - This copies the executable to `C:\\Program Files\\VPN Kill Switch`, creates shortcuts, and registers in Add/Remove Programs.
2. **Option 2: Use `installer.py`**:
   ```bash
   python installer.py
   ```
   Run as administrator to ensure proper installation.
3. **Verify Installation**:
   - Check `C:\\Program Files\\VPN Kill Switch\\VPN_KillSwitch_Config.exe`.
   - Confirm desktop shortcut (`VPN Kill Switch.lnk`).
   - Confirm start menu shortcut (`%USERPROFILE%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\VPN Kill Switch`).
   - Check registry: `HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\VPN Kill Switch`.

### Step 3: Testing After Deployment
1. **Configure Kill Switch**:
   - Set VPN processes (e.g., `surfshark.exe`) and network interface in the **Configuration** tab.
   - Save configuration.
2. **Test Kill Switch**:
   - Start the service in the **Service Management** tab.
   - Close your VPN (e.g., Surfshark) and verify internet access is blocked.
   - Start the VPN and confirm internet access is restored.
   - Check `%USERPROFILE%\\vpn_killswitch.log` for entries like:
     ```
     2025-06-27 18:40:00,123 - INFO - Kill switch service started
     2025-06-27 18:40:05,456 - INFO - No VPN processes detected, disabling network
     ```
3. **Test Installation**:
   - Click **Install to Startup**, verify shortcuts and registry entry.
   - Click **Remove from Startup**, confirm removal of shortcuts and registry.

### Step 4: Uninstall
1. **Option 1: Use GUI**:
   - In the **Service Management** tab, click **Remove from Startup**.
   - This deletes shortcuts, registry entries, and the installation directory (`C:\\Program Files\\VPN Kill Switch`).
2. **Option 2: Manual Uninstallation**:
   - Delete `C:\\Program Files\\VPN Kill Switch`.
   - Remove shortcuts from Desktop and `%USERPROFILE%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\VPN Kill Switch`.
   - Delete registry key: `HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\VPN Kill Switch`.

## Configuration
- **Config File**: `%USERPROFILE%\\vpn_killswitch_config.json`
- **Default Settings**:
  ```json
  {
      "vpn_processes": ["surfshark.exe", "nordvpn.exe", "expressvpn.exe"],
      "vpn_name": "My VPN",
      "network_interface": "Wi-Fi",
      "startup_delay": 5,
      "check_interval": 3,
      "enabled": true,
      "log_level": "INFO"
  }
  ```
- **Log File**: `%USERPROFILE%\\vpn_killswitch.log` (view via **Open Log File** button).

## Log Rotation
To manage log file size, add the following to `vpn_killswitch_gui.py`’s `__init__`:
```python
from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler(
    filename=str(Path.home() / "vpn_killswitch.log"),
    maxBytes=1024*1024,  # 1 MB
    backupCount=5
)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logging.getLogger().addHandler(handler)
```

## Troubleshooting

### "Not recognized as an internal or external command"
- Ensure Python and `pip` are in PATH:
  ```bash
  set PATH=%PATH%;C:\\Python39;C:\\Python39\\Scripts
  ```
- Verify installation: `python --version`, `pip --version`.

### "Access Denied" Errors
- Run Command Prompt, `build.bat`, or executable as administrator.
- Disable antivirus temporarily or add an exception for `dist\\VPN_KillSwitch_Config.exe`.

### "Module not found" Errors
- Install missing modules: `pip install <module_name>`.
- Add to `hiddenimports` in `setup.py` and `VPN_KillSwitch_Config.spec` if needed.
- Common issue: `ModuleNotFoundError: collections.abc` – add `--hidden-import=collections.abc`.

### Network Interface Issues
- Verify interface name:
  ```bash
  netsh interface show interface
  ```
- Update `network_interface` in the GUI or config file.

### Command Prompt Flashing
- Should be resolved with `CREATE_NO_WINDOW`. If flashing persists, check `%USERPROFILE%\\vpn_killswitch.log` for unexpected subprocess calls.

### Installation Failures
- Ensure `pywin32` is installed: `pip show pywin32`.
- Run installer as administrator.
- Check log file for errors like `Failed to create desktop shortcut`.

## Files Included
- `vpn_killswitch_gui.py`: Main application with GUI and kill switch logic.
- `main.py`: Utility to regenerate build files (optional).
- `setup.py`: PyInstaller configuration.
- `VPN_KillSwitch_Config.spec`: PyInstaller specification file.
- `build.bat`: Automated build script.
- `requirements.txt`: Python dependencies.
- `manifest.xml`: Windows UAC manifest.
- `installer.py`: System installer for shortcuts and registry.

## Notes
- **Version**: 1.0.0 (update as needed).
- **Administrator Privileges**: The executable requires admin rights for network control and installation.
- **Windows Defender**: May flag the executable; add an exception if needed.
- **Windows Only**: The tool is designed for Windows 10+.

## Support
For issues, check `%USERPROFILE%\\vpn_killswitch.log` or submit an issue at [GitHub repository URL] (replace with your repo URL).
'''

    # WRITE ALL FILES
    files_to_create: dict[str, str] = {
        'setup.py': setup_py_content,
        'manifest.xml': manifest_content,
        'requirements.txt': requirements_content,
        'build.bat': build_script_content,
        'installer.py': installer_script_content,
        'README.md': readme_content
    }

    for filename, content in files_to_create.items():
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created: {filename}")

    print("\nAll setup files created successfully!")
    print("\nTo build the executable:")
    print("1. Run 'build.bat' as administrator")
    print("2. Or run 'python setup.py'")
    print("\nThe executable will be created in the 'dist' folder.")


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================
def main() -> None:
    """
    Main function to run the setup file creation process.

    Initializes the installer and generates all setup files.
    """
    # SETUP FILE CREATION
    create_setup_files()


# ============================================================================
# PROGRAM EXECUTION GUARD
# ============================================================================
if __name__ == "__main__":
    # Execute main function only when script is run directly
    main()
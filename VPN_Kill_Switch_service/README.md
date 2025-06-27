# VPN Kill Switch Configuration Tool

## Overview
The VPN Kill Switch Configuration Tool is a Windows application that ensures your internet connection is disabled when your VPN is not active, preventing unprotected network access. It provides a graphical interface for configuring VPN processes, monitoring network status, and managing the kill switch service.

## Features
- **Configuration**: Set VPN processes (e.g., `surfshark.exe`), network interface, and monitoring intervals.
- **Real-Time Monitoring**: Displays service, VPN, and network status.
- **Kill Switch**: Automatically disables the network when no VPN processes are detected.
- **Logging**: Logs events to `%USERPROFILE%\vpn_killswitch.log` for debugging.
- **Installation**: Installs to `C:\Program Files\VPN Kill Switch` with desktop and start menu shortcuts.
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
   .venv\Scripts\activate
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
1. **Locate Executable**: Find `dist\VPN_KillSwitch_Config.exe`.
2. **Run as Administrator**: Right-click and select **Run as administrator** (required for network control and installation).
3. **Verify Functionality**:
   - **Configuration Tab**: Set VPN processes (e.g., `surfshark.exe`), network interface (check with `netsh interface show interface`), and save.
   - **Status Tab**: Confirm service, VPN, and network status updates.
   - **Service Management Tab**: Start/stop the kill switch, test network block, or install to startup.

### Step 2: Install System-Wide
1. **Option 1: Use GUI**:
   - In the **Service Management** tab, click **Install to Startup**.
   - This copies the executable to `C:\Program Files\VPN Kill Switch`, creates shortcuts, and registers in Add/Remove Programs.
2. **Option 2: Use `installer.py`**:
   ```bash
   python installer.py
   ```
   Run as administrator to ensure proper installation.
3. **Verify Installation**:
   - Check `C:\Program Files\VPN Kill Switch\VPN_KillSwitch_Config.exe`.
   - Confirm desktop shortcut (`VPN Kill Switch.lnk`).
   - Confirm start menu shortcut (`%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\VPN Kill Switch`).
   - Check registry: `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\VPN Kill Switch`.

### Step 3: Testing After Deployment
1. **Configure Kill Switch**:
   - Set VPN processes (e.g., `surfshark.exe`) and network interface in the **Configuration** tab.
   - Save configuration.
2. **Test Kill Switch**:
   - Start the service in the **Service Management** tab.
   - Close your VPN (e.g., Surfshark) and verify internet access is blocked.
   - Start the VPN and confirm internet access is restored.
   - Check `%USERPROFILE%\vpn_killswitch.log` for entries like:
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
   - This deletes shortcuts, registry entries, and the installation directory (`C:\Program Files\VPN Kill Switch`).
2. **Option 2: Manual Uninstallation**:
   - Delete `C:\Program Files\VPN Kill Switch`.
   - Remove shortcuts from Desktop and `%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\VPN Kill Switch`.
   - Delete registry key: `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\VPN Kill Switch`.

## Configuration
- **Config File**: `%USERPROFILE%\vpn_killswitch_config.json`
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
- **Log File**: `%USERPROFILE%\vpn_killswitch.log` (view via **Open Log File** button).

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
  set PATH=%PATH%;C:\Python39;C:\Python39\Scripts
  ```
- Verify installation: `python --version`, `pip --version`.

### "Access Denied" Errors
- Run Command Prompt, `build.bat`, or executable as administrator.
- Disable antivirus temporarily or add an exception for `dist\VPN_KillSwitch_Config.exe`.

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
- Should be resolved with `CREATE_NO_WINDOW`. If flashing persists, check `%USERPROFILE%\vpn_killswitch.log` for unexpected subprocess calls.

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
For issues, check `%USERPROFILE%\vpn_killswitch.log` or submit an issue at [GitHub repository URL] (replace with your repo URL).

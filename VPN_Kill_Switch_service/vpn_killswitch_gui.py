# ============================================================================
# VPN KILL SWITCH CONFIGURATION TOOL
# ============================================================================
# A GUI-based application for configuring and managing a VPN kill switch.
# Monitors VPN processes (e.g., surfshark.exe) and disables network access
# when no VPN is active. Includes logging, status monitoring, and installation.
# ============================================================================

# IMPORT REQUIRED LIBRARIES
import tkinter as tk  # Core GUI framework
from tkinter import ttk, messagebox  # GUI components for tabs and dialogs
import json  # JSON configuration handling
import os  # Operating system interfaces
from pathlib import Path  # Filesystem path operations
import psutil  # Process monitoring
import threading  # Thread-based monitoring
import time  # Timing operations
import logging  # Logging functionality
from logging.handlers import RotatingFileHandler  # Log rotation
import subprocess  # Subprocess execution for netsh commands
import shutil  # File operations for installation
import winreg  # Windows registry access
try:
    import win32com.client  # For creating shortcuts
except ImportError:
    win32com = None  # Handle missing pywin32 gracefully

# WINDOWS-SPECIFIC CONSTANT
# Flag to suppress command prompt window during subprocess execution
CREATE_NO_WINDOW: int = 0x08000000


# ============================================================================
# MAIN APPLICATION CLASS
# ============================================================================
class VPNKillSwitchConfigGUI:
    """
    A GUI application for configuring and managing a VPN kill switch.

    This class creates a Tkinter-based interface that allows users to:
    - Configure VPN processes, network interface, and monitoring intervals
    - Start/stop a kill switch service that disables network if VPN is inactive
    - View real-time status of service, VPN, and network
    - Save/load configurations, view logs, and install to system
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the VPN Kill Switch application with GUI components.

        Args:
            root (tk.Tk): The main Tkinter window instance.
        """
        # MAIN WINDOW SETUP
        # Configure window title and size, make non-resizable
        self.root: tk.Tk = root
        self.root.title("VPN Kill Switch - Configuration")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        # CONFIGURATION FILE PATH
        # Store configuration in user's home directory
        self.config_path: Path = Path.home() / "vpn_killswitch_config.json"

        # LOGGING INITIALIZATION
        # Set up logging with configurable level and rotation
        log_levels: dict = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR
        }
        self.config: dict = self.load_config()
        log_level: int = log_levels.get(self.config.get("log_level", "INFO"), logging.INFO)
        log_file: Path = Path.home() / "vpn_killswitch.log"
        handler = RotatingFileHandler(
            filename=str(log_file),
            maxBytes=1024*1024,  # 1 MB
            backupCount=5
        )
        handler.setLevel(log_level)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logging.getLogger().addHandler(handler)
        logging.info("VPN Kill Switch Configuration Tool started")

        # KILL SWITCH THREAD INITIALIZATION
        # Initialize variables for kill switch monitoring thread
        self.kill_switch_running: bool = False
        self.kill_switch_thread: threading.Thread | None = None
        self.last_network_status: str | None = None  # Cache network status
        self.last_vpn_status: bool | None = None  # Cache VPN status

        # INSTALLER SETTINGS
        # Define installation paths and names
        self.app_name: str = "VPN Kill Switch"
        self.exe_name: str = "VPN_KillSwitch_Config.exe"
        self.default_install_path: Path = Path("C:/Program Files") / self.app_name

        # GUI SETUP
        # Initialize all GUI components
        self.setup_gui()
        self.load_values()

        # STATUS MONITORING INITIALIZATION
        # Start background thread for periodic status updates
        self.start_status_monitoring()

    # ============================================================================
    # CONFIGURATION MANAGEMENT - LOAD
    # ============================================================================
    def load_config(self) -> dict:
        """
        Load configuration from JSON file or return default config.

        Returns:
            dict: Configuration dictionary with VPN and kill switch settings.

        Raises:
            Exception: If there is an error reading the configuration file.
        """
        # DEFAULT CONFIGURATION
        # Define fallback configuration values
        default_config: dict = {
            "vpn_processes": ["surfshark.exe", "nordvpn.exe", "expressvpn.exe"],
            "vpn_name": "My VPN",
            "network_interface": "Wi-Fi",
            "startup_delay": 5,
            "check_interval": 3,
            "enabled": True,
            "log_level": "INFO"
        }

        # CONFIG FILE READING
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding="utf-8") as file:
                    config: dict = json.load(file)
                    default_config.update(config)
        except Exception as e:
            logging.error(f"Failed to load config: {e}")

        return default_config

    # ============================================================================
    # CONFIGURATION MANAGEMENT - SAVE
    # ============================================================================
    def save_config(self) -> bool:
        """
        Save configuration to JSON file.

        Returns:
            bool: True if save is successful, False otherwise.

        Raises:
            Exception: If there is an error writing to the configuration file.
        """
        # CONFIG FILE WRITING
        try:
            with open(self.config_path, 'w', encoding="utf-8") as file:
                json.dump(self.config, file, indent=4)
            return True
        except Exception as e:
            logging.error(f"Failed to save config: {e}")
            return False

    # ============================================================================
    # GUI SETUP
    # ============================================================================
    def setup_gui(self) -> None:
        """
        Set up the GUI components for the application.

        Creates a tabbed interface with Configuration, Status, and Service Management tabs.
        """
        # NOTEBOOK CREATION
        # Create tabbed interface for organizing GUI components
        notebook: ttk.Notebook = ttk.Notebook(self.root)
        notebook.pack(pady=10, expand=True, fill="both")

        # CONFIGURATION TAB SETUP
        # Create frame for configuration settings
        config_frame: ttk.Frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="Configuration")

        # VPN NAME INPUT
        ttk.Label(config_frame, text="VPN Display Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.vpn_name_var: tk.StringVar = tk.StringVar()
        ttk.Entry(config_frame, textvariable=self.vpn_name_var).grid(row=0, column=1, padx=5, pady=5)

        # VPN PROCESS NAMES INPUT
        # Text area for entering multiple VPN process names
        ttk.Label(config_frame, text="VPN Process Names (one per line):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.vpn_processes_text: tk.Text = tk.Text(config_frame, height=4, width=30)
        self.vpn_processes_text.grid(row=1, column=1, padx=5, pady=5)

        # NETWORK INTERFACE SELECTION
        # Combobox for selecting network interface
        ttk.Label(config_frame, text="Network Interface:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.interface_var: tk.StringVar = tk.StringVar()
        self.interface_combo: ttk.Combobox = ttk.Combobox(config_frame, textvariable=self.interface_var, values=self.get_network_interfaces())
        self.interface_combo.grid(row=2, column=1, padx=5, pady=5)

        # STARTUP DELAY INPUT
        ttk.Label(config_frame, text="Startup Delay (seconds):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.startup_delay_var: tk.StringVar = tk.StringVar()
        ttk.Entry(config_frame, textvariable=self.startup_delay_var).grid(row=3, column=1, padx=5, pady=5)

        # CHECK INTERVAL INPUT
        ttk.Label(config_frame, text="Check Interval (seconds):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.check_interval_var: tk.StringVar = tk.StringVar()
        ttk.Entry(config_frame, textvariable=self.check_interval_var).grid(row=4, column=1, padx=5, pady=5)

        # KILL SWITCH ENABLE CHECKBOX
        self.enabled_var: tk.BooleanVar = tk.BooleanVar()
        ttk.Checkbutton(config_frame, text="Enable Kill Switch", variable=self.enabled_var).grid(row=5, column=0, columnspan=2, pady=5)

        # LOG LEVEL SELECTION
        ttk.Label(config_frame, text="Log Level:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.log_level_var: tk.StringVar = tk.StringVar()
        ttk.Combobox(config_frame, textvariable=self.log_level_var, values=["DEBUG", "INFO", "WARNING", "ERROR"]).grid(row=6, column=1, padx=5, pady=5)

        # SAVE CONFIGURATION BUTTON
        ttk.Button(config_frame, text="Save Configuration", command=self.save_configuration).grid(row=7, column=0, columnspan=2, pady=10)

        # STATUS TAB SETUP
        # Create frame for status display
        status_frame: ttk.Frame = ttk.Frame(notebook)
        notebook.add(status_frame, text="Status")

        # SERVICE STATUS LABEL
        self.service_status_label: ttk.Label = ttk.Label(status_frame, text="Service: Stopped ✗", foreground="red")
        self.service_status_label.pack(pady=5)

        # VPN STATUS LABEL
        self.vpn_status_label: ttk.Label = ttk.Label(status_frame, text="VPN: Not Connected ✗", foreground="red")
        self.vpn_status_label.pack(pady=5)

        # NETWORK STATUS LABEL
        self.network_status_label: ttk.Label = ttk.Label(status_frame, text="Network: Active", foreground="blue")
        self.network_status_label.pack(pady=5)

        # VPN PROCESSES LIST
        ttk.Label(status_frame, text="Running VPN Processes:").pack(pady=5)
        self.processes_listbox: tk.Listbox = tk.Listbox(status_frame, height=5, width=50)
        self.processes_listbox.pack(pady=5)

        # LOG ENTRIES DISPLAY
        ttk.Label(status_frame, text="Recent Log Entries:").pack(pady=5)
        self.log_text: tk.Text = tk.Text(status_frame, height=5, width=50, state="disabled")
        self.log_text.pack(pady=5)

        # REFRESH BUTTON
        ttk.Button(status_frame, text="Refresh", command=self.update_status).pack(pady=5)

        # SERVICE MANAGEMENT TAB SETUP
        # Create frame for service control buttons
        service_frame: ttk.Frame = ttk.Frame(notebook)
        notebook.add(service_frame, text="Service Management")

        # SERVICE CONTROL BUTTONS
        ttk.Button(service_frame, text="Install to Startup", command=self.install_startup).pack(pady=5)
        ttk.Button(service_frame, text="Remove from Startup", command=self.uninstall_startup).pack(pady=5)
        ttk.Button(service_frame, text="Start Service", command=self.start_service).pack(pady=5)
        ttk.Button(service_frame, text="Stop Service", command=self.stop_service).pack(pady=5)
        ttk.Button(service_frame, text="Open Log File", command=self.open_log_file).pack(pady=5)
        ttk.Button(service_frame, text="Test Network Block", command=self.test_network_block).pack(pady=5)
        ttk.Button(service_frame, text="Apply & Restart Service", command=self.apply_and_restart).pack(pady=5)

    # ============================================================================
    # NETWORK INTERFACE MANAGEMENT
    # ============================================================================
    def get_network_interfaces(self) -> list[str]:
        """
        Get list of available network interfaces.

        Returns:
            list[str]: List of network interface names.

        Raises:
            Exception: If there is an error retrieving network interfaces.
        """
        # NETWORK INTERFACE ENUMERATION
        try:
            interfaces: list[str] = []
            for iface in psutil.net_if_addrs().keys():
                interfaces.append(iface)
            return interfaces
        except Exception as e:
            logging.error(f"Failed to get network interfaces: {e}")
            return ["Wi-Fi", "Ethernet"]

    # ============================================================================
    # CONFIGURATION MANAGEMENT - GUI INPUT LOADING
    # ============================================================================
    def load_values(self) -> None:
        """
        Load configuration values into GUI components.
        """
        # POPULATE GUI FIELDS
        self.vpn_name_var.set(self.config.get("vpn_name", ""))
        self.vpn_processes_text.delete(1.0, tk.END)
        self.vpn_processes_text.insert(tk.END, "\n".join(self.config.get("vpn_processes", [])))
        self.interface_var.set(self.config.get("network_interface", "Wi-Fi"))
        self.startup_delay_var.set(str(self.config.get("startup_delay", 5)))
        self.check_interval_var.set(str(self.config.get("check_interval", 3)))
        self.enabled_var.set(self.config.get("enabled", True))
        self.log_level_var.set(self.config.get("log_level", "INFO"))

    # ============================================================================
    # CONFIGURATION MANAGEMENT - SAVE FROM GUI
    # ============================================================================
    def save_configuration(self) -> None:
        """
        Save configuration from GUI inputs to the config file.

        Raises:
            ValueError: If numeric inputs (startup_delay, check_interval) are invalid.
            Exception: If there is an error saving the configuration.
        """
        # CONFIG VALIDATION AND SAVING
        try:
            self.config["enabled"] = self.enabled_var.get()
            self.config["vpn_name"] = self.vpn_name_var.get()
            self.config["network_interface"] = self.interface_var.get()
            self.config["startup_delay"] = int(self.startup_delay_var.get())
            self.config["check_interval"] = int(self.check_interval_var.get())
            self.config["log_level"] = self.log_level_var.get()

            processes_text: str = self.vpn_processes_text.get(1.0, tk.END).strip()
            self.config["vpn_processes"] = [p.strip() for p in processes_text.split("\n") if p.strip()]

            # SAVE CONFIGURATION
            if self.save_config():
                logging.info("Configuration saved successfully")
                messagebox.showinfo("Success", "Configuration saved successfully!")
                # UPDATE LOGGING LEVEL
                log_levels: dict = {
                    "DEBUG": logging.DEBUG,
                    "INFO": logging.INFO,
                    "WARNING": logging.WARNING,
                    "ERROR": logging.ERROR
                }
                logging.getLogger().setLevel(log_levels.get(self.config["log_level"], logging.INFO))
            else:
                logging.error("Failed to save configuration")
                messagebox.showerror("Error", "Failed to save configuration")
        except ValueError as e:
            logging.error(f"Validation error: {e}")
            messagebox.showerror("Validation Error", "Please check your numeric values!")
        except Exception as e:
            logging.error(f"Failed to save configuration: {e}")
            messagebox.showerror("Error", f"Failed to save configuration: {e}")

    # ============================================================================
    # PROCESS MONITORING
    # ============================================================================
    def get_vpn_processes(self) -> list[dict]:
        """
        Get list of running VPN processes.

        Returns:
            list[dict]: List of dictionaries containing process names and PIDs.

        Raises:
            Exception: If there is an error retrieving process information.
        """
        # PROCESS ENUMERATION
        vpn_processes: list[dict] = []
        try:
            for proc in psutil.process_iter(['name', 'pid']):
                if proc.info['name'].lower() in [p.lower() for p in self.config.get("vpn_processes", [])]:
                    vpn_processes.append(proc.info)
        except Exception as e:
            logging.error(f"Failed to get VPN processes: {e}")
        return vpn_processes

    # ============================================================================
    # SERVICE STATUS CHECK
    # ============================================================================
    def is_service_running(self) -> bool:
        """
        Check if the kill switch service is running.

        Returns:
            bool: True if the service is running, False otherwise.
        """
        return self.kill_switch_running

    # ============================================================================
    # NETWORK INTERFACE CONTROL
    # ============================================================================
    def toggle_network_interface(self, enable: bool = True) -> bool:
        """
        Enable or disable the network interface using netsh.

        Args:
            enable (bool): True to enable the interface, False to disable.

        Returns:
            bool: True if the operation is successful, False otherwise.

        Raises:
            subprocess.CalledProcessError: If the netsh command fails.
            Exception: For other unexpected errors.
        """
        # NETWORK INTERFACE TOGGLING
        try:
            interface: str = self.config.get("network_interface", "Wi-Fi")
            action: str = "enable" if enable else "disable"
            cmd: list[str] = ["netsh", "interface", "set", "interface", interface, action]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, creationflags=CREATE_NO_WINDOW)
            logging.info(f"Network interface '{interface}' {action}d successfully")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to {action} network interface '{interface}': {e.stderr}")
            return False
        except Exception as e:
            logging.error(f"Error toggling network interface: {e}")
            return False

    # ============================================================================
    # KILL SWITCH MONITORING
    # ============================================================================
    def kill_switch_monitor(self) -> None:
        """
        Monitor VPN processes and toggle network interface accordingly.

        Disables the network if no VPN processes are detected and enables it when
        VPN processes are active. Runs in a separate thread.
        """
        # MONITOR INITIALIZATION
        logging.info(f"Kill switch monitor started with startup delay of {self.config['startup_delay']} seconds")
        time.sleep(self.config.get("startup_delay", 5))  # Wait for startup delay
        last_vpn_status: bool | None = None

        # MONITOR LOOP
        while self.kill_switch_running:
            if not self.config.get("enabled", True):
                logging.info("Kill switch disabled in configuration, skipping check")
                time.sleep(self.config.get("check_interval", 3))
                continue

            # VPN PROCESS CHECK
            vpn_processes: list[dict] = self.get_vpn_processes()
            current_vpn_status: bool = bool(vpn_processes)

            # NETWORK TOGGLE ON STATUS CHANGE
            if current_vpn_status != last_vpn_status:
                if vpn_processes:
                    logging.info(f"VPN detected: {[p['name'] for p in vpn_processes]}, enabling network")
                    self.toggle_network_interface(True)
                else:
                    logging.info("No VPN processes detected, disabling network")
                    self.toggle_network_interface(False)
                last_vpn_status = current_vpn_status

            time.sleep(self.config.get("check_interval", 3))

        # MONITOR SHUTDOWN
        logging.info("Kill switch monitor stopped")

    # ============================================================================
    # SERVICE MANAGEMENT - START
    # ============================================================================
    def start_service(self) -> None:
        """
        Start the kill switch monitoring service.

        Raises:
            Exception: If there is an error starting the service.
        """
        # SERVICE STARTUP
        try:
            if not self.is_service_running():
                if not self.config.get("enabled", True):
                    logging.warning("Cannot start service: Kill switch is disabled in configuration")
                    messagebox.showwarning("Warning", "Kill switch is disabled in configuration")
                    return
                self.kill_switch_running = True
                self.kill_switch_thread = threading.Thread(target=self.kill_switch_monitor, daemon=True)
                self.kill_switch_thread.start()
                logging.info("Kill switch service started")
                messagebox.showinfo("Service", "Kill switch service started")
            else:
                logging.info("Kill switch service already running")
                messagebox.showinfo("Service", "Kill switch service already running")
        except Exception as e:
            logging.error(f"Failed to start service: {e}")
            messagebox.showerror("Error", f"Failed to start service: {e}")

    # ============================================================================
    # SERVICE MANAGEMENT - STOP
    # ============================================================================
    def stop_service(self) -> None:
        """
        Stop the kill switch monitoring service.

        Raises:
            Exception: If there is an error stopping the service.
        """
        # SERVICE SHUTDOWN
        try:
            if self.is_service_running():
                self.kill_switch_running = False
                if self.kill_switch_thread:
                    self.kill_switch_thread.join(timeout=5)
                self.toggle_network_interface(True)  # Ensure network is enabled
                logging.info("Kill switch service stopped")
                messagebox.showinfo("Service", "Kill switch service stopped")
            else:
                logging.info("Kill switch service not running")
                messagebox.showinfo("Service", "Kill switch service not running")
        except Exception as e:
            logging.error(f"Failed to stop service: {e}")
            messagebox.showerror("Error", f"Failed to stop service: {e}")

    # ============================================================================
    # STARTUP MANAGEMENT - INSTALL
    # ============================================================================
    def install_startup(self) -> None:
        """
        Install the application to run at system startup.

        Copies the executable to Program Files, creates shortcuts, and registers
        the program in Windows Add/Remove Programs.

        Raises:
            Exception: If there is an error during installation.
        """
        # INSTALLATION SETUP
        try:
            # DETERMINE EXECUTABLE PATH
            import sys
            exe_source: Path = Path(sys.executable) if getattr(sys, 'frozen', False) else Path("dist") / self.exe_name
            install_path: Path = self.default_install_path

            # CREATE INSTALLATION DIRECTORY
            install_path.mkdir(parents=True, exist_ok=True)

            # COPY EXECUTABLE
            exe_dest: Path = install_path / self.exe_name
            if exe_source.exists():
                shutil.copy2(exe_source, exe_dest)
                logging.info(f"Installed to: {exe_dest}")

                # CREATE SHORTCUTS
                self.create_desktop_shortcut(exe_dest)
                self.create_start_menu_shortcut(exe_dest)

                # REGISTER PROGRAM
                self.register_program(install_path)

                logging.info("Installation completed successfully")
                messagebox.showinfo("Success", "Application installed successfully!\nYou can run it from the Desktop or Start Menu.")
            else:
                logging.error(f"Executable not found: {exe_source}")
                messagebox.showerror("Error", f"Executable not found: {exe_source}")

        except Exception as e:
            logging.error(f"Installation failed: {e}")
            messagebox.showerror("Error", f"Installation failed: {e}")

    # ============================================================================
    # STARTUP MANAGEMENT - UNINSTALL
    # ============================================================================
    def uninstall_startup(self) -> None:
        """
        Remove the application from system startup and clean up installation.

        Deletes shortcuts, registry entries, and installation directory.

        Raises:
            Exception: If there is an error during uninstallation.
        """
        # UNINSTALLATION SETUP
        try:
            install_path: Path = self.default_install_path

            # REMOVE SHORTCUTS
            self.remove_desktop_shortcut()
            self.remove_start_menu_shortcut()

            # REMOVE REGISTRY ENTRY
            self.remove_program_registry()

            # REMOVE INSTALLATION DIRECTORY
            if install_path.exists():
                shutil.rmtree(install_path, ignore_errors=True)
                logging.info(f"Removed installation directory: {install_path}")

            logging.info("Uninstallation completed successfully")
            messagebox.showinfo("Success", "Application uninstalled successfully!")

        except Exception as e:
            logging.error(f"Uninstallation failed: {e}")
            messagebox.showerror("Error", f"Uninstallation failed: {e}")

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
        if not win32com:
            logging.warning("pywin32 not available - skipping desktop shortcut")
            return
        try:
            desktop: Path = Path.home() / "Desktop"
            shortcut_path: Path = desktop / f"{self.app_name}.lnk"

            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(exe_path)
            shortcut.WorkingDirectory = str(exe_path.parent)
            shortcut.Description = "VPN Kill Switch Configuration Tool"
            shortcut.save()

            logging.info(f"Desktop shortcut created: {shortcut_path}")

        except Exception as e:
            logging.error(f"Failed to create desktop shortcut: {e}")

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
        if not win32com:
            logging.warning("pywin32 not available - skipping start menu shortcut")
            return
        try:
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

            logging.info(f"Start menu shortcut created: {shortcut_path}")

        except Exception as e:
            logging.error(f"Failed to create start menu shortcut: {e}")

    # ============================================================================
    # SHORTCUT REMOVAL - DESKTOP
    # ============================================================================
    def remove_desktop_shortcut(self) -> None:
        """
        Remove the desktop shortcut for the application.

        Raises:
            Exception: If there is an error removing the shortcut.
        """
        # DESKTOP SHORTCUT REMOVAL
        try:
            desktop: Path = Path.home() / "Desktop"
            shortcut_path: Path = desktop / f"{self.app_name}.lnk"
            if shortcut_path.exists():
                shortcut_path.unlink()
                logging.info(f"Removed desktop shortcut: {shortcut_path}")

        except Exception as e:
            logging.error(f"Failed to remove desktop shortcut: {e}")

    # ============================================================================
    # SHORTCUT REMOVAL - START MENU
    # ============================================================================
    def remove_start_menu_shortcut(self) -> None:
        """
        Remove the start menu shortcut for the application.

        Raises:
            Exception: If there is an error removing the shortcut.
        """
        # START MENU SHORTCUT REMOVAL
        try:
            start_menu: Path = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
            app_folder: Path = start_menu / self.app_name
            shortcut_path: Path = app_folder / f"{self.app_name}.lnk"
            if shortcut_path.exists():
                shortcut_path.unlink()
                logging.info(f"Removed start menu shortcut: {shortcut_path}")
            if app_folder.exists() and not any(app_folder.iterdir()):
                app_folder.rmdir()
                logging.info(f"Removed start menu folder: {app_folder}")

        except Exception as e:
            logging.error(f"Failed to remove start menu shortcut: {e}")

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
            key_path: str = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\\" + self.app_name

            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, self.app_name)
                winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, "1.0.0")
                winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, "VPN Kill Switch")
                winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, str(install_path))
                winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, str(install_path / self.exe_name))
                winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, f'"{install_path / self.exe_name}" --uninstall')
                winreg.SetValueEx(key, "NoModify", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "NoRepair", 0, winreg.REG_DWORD, 1)

            logging.info("Program registered in Add/Remove Programs")

        except Exception as e:
            logging.error(f"Failed to register program: {e}")

    # ============================================================================
    # PROGRAM UNREGISTRATION
    # ============================================================================
    def remove_program_registry(self) -> None:
        """
        Remove the program from Windows Add/Remove Programs.

        Raises:
            Exception: If there is an error accessing the Windows registry.
        """
        # REGISTRY REMOVAL
        try:
            key_path: str = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\\" + self.app_name
            winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            logging.info("Program unregistered from Add/Remove Programs")

        except Exception as e:
            logging.error(f"Failed to unregister program: {e}")

    # ============================================================================
    # NETWORK TESTING
    # ============================================================================
    def test_network_block(self) -> None:
        """
        Test network blocking functionality by temporarily disabling the network.

        Raises:
            Exception: If there is an error during the network block test.
        """
        # NETWORK BLOCK TEST
        try:
            result: bool = messagebox.askyesno("Test Network Block", "This will temporarily disable network access for 5 seconds. Continue?")
            if result:
                logging.info("Testing network block")
                self.toggle_network_interface(False)
                messagebox.showinfo("Test", "Network disabled. Re-enabling in 5 seconds...")
                time.sleep(5)
                self.toggle_network_interface(True)
                logging.info("Network block test completed")
                messagebox.showinfo("Test", "Network block test completed")
        except Exception as e:
            logging.error(f"Failed to test network block: {e}")
            messagebox.showerror("Error", f"Failed to test network block: {e}")

    # ============================================================================
    # SERVICE MANAGEMENT - APPLY AND RESTART
    # ============================================================================
    def apply_and_restart(self) -> None:
        """
        Apply configuration changes and restart the kill switch service.
        """
        # CONFIG APPLICATION AND SERVICE RESTART
        logging.info("Applying configuration and restarting service")
        self.save_configuration()
        self.stop_service()
        time.sleep(1)
        self.start_service()

    # ============================================================================
    # LOG FILE ACCESS
    # ============================================================================
    def open_log_file(self) -> None:
        """
        Open the log file in the default text editor.

        Raises:
            Exception: If there is an error opening the log file.
        """
        # LOG FILE OPENING
        try:
            log_path: Path = Path.home() / "vpn_killswitch.log"
            logging.info(f"Attempting to open log file: {log_path}")
            if log_path.exists():
                os.startfile(str(log_path))
            else:
                logging.error("Log file not found")
                messagebox.showinfo("Log File", "Log file not found")
        except Exception as e:
            logging.error(f"Failed to open log file: {e}")
            messagebox.showerror("Error", f"Failed to open log file: {e}")

    # ============================================================================
    # STATUS MONITORING
    # ============================================================================
    def update_status(self) -> None:
        """
        Update the status display in the GUI.

        Checks service, VPN, and network status, and updates GUI labels and lists.
        Caches network status to reduce subprocess calls.

        Raises:
            Exception: If there is an error updating the status.
        """
        # STATUS UPDATE
        try:
            # SERVICE STATUS CHECK
            service_running: bool = self.is_service_running()
            if service_running:
                service_status: str = "Service: Running ✓"
                service_color: str = "green"
            else:
                service_status: str = "Service: Stopped ✗"
                service_color: str = "red"

            # VPN STATUS CHECK
            vpn_processes: list[dict] = self.get_vpn_processes()
            if vpn_processes:
                vpn_status: str = f"VPN: Connected ({len(vpn_processes)} processes) ✓"
                vpn_color: str = "green"
                logging.info(f"VPN processes running: {[p['name'] for p in vpn_processes]}")
            else:
                vpn_status: str = "VPN: Not Connected ✗"
                vpn_color: str = "red"
                logging.info("No VPN processes running (e.g., surfshark.exe, nordvpn.exe, expressvpn.exe)")

            # NETWORK STATUS CHECK
            # Only run netsh if VPN status changed or first run
            network_status: str = "Network: Unknown"
            network_color: str = "gray"
            current_vpn_status: bool = bool(vpn_processes)
            if self.last_network_status is None or self.last_vpn_status != current_vpn_status:
                try:
                    interface: str = self.config.get("network_interface", "Wi-Fi")
                    cmd: list[str] = ["netsh", "interface", "show", "interface", interface]
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True, creationflags=CREATE_NO_WINDOW)
                    if "Enabled" in result.stdout:
                        network_status = "Network: Active"
                        network_color = "blue"
                    else:
                        network_status = "Network: Disabled"
                        network_color = "red"
                    logging.info(f"Network interface '{interface}' status: {network_status}")
                    self.last_network_status = network_status
                except Exception as e:
                    logging.error(f"Failed to check network status: {e}")
                    network_status = "Network: Unknown"
                    network_color = "gray"
            else:
                network_status = self.last_network_status
                network_color = "blue" if "Active" in network_status else "red"

            self.last_vpn_status = current_vpn_status

            # LOG ENTRIES READING
            log_entries: list[str] = []
            log_path: Path = Path.home() / "vpn_killswitch.log"
            if log_path.exists():
                with open(log_path, 'r', encoding="utf-8") as f:
                    log_entries = f.readlines()[-10:]  # Get last 10 lines
                logging.info("Updated status display")
            else:
                log_entries = ["Log file not found"]
                logging.error("Log file not found during status update")

            # GUI UPDATE
            # Schedule thread-safe GUI update
            self.root.after(0, self.update_status_labels,
                            service_status, service_color,
                            vpn_status, vpn_color,
                            network_status, network_color,
                            vpn_processes, log_entries)

        except Exception as e:
            logging.error(f"Status update error: {e}")
            print(f"Status update error: {e}")

    # ============================================================================
    # GUI STATUS UPDATE
    # ============================================================================
    def update_status_labels(self, service_status: str, service_color: str, vpn_status: str, vpn_color: str,
                            network_status: str, network_color: str, vpn_processes: list[dict], log_entries: list[str]) -> None:
        """
        Update GUI labels and lists with status information.

        Args:
            service_status (str): Text for service status label.
            service_color (str): Color for service status label.
            vpn_status (str): Text for VPN status label.
            vpn_color (str): Color for VPN status label.
            network_status (str): Text for network status label.
            network_color (str): Color for network status label.
            vpn_processes (list[dict]): List of running VPN processes.
            log_entries (list[str]): Recent log entries to display.
        """
        # UPDATE LABELS
        self.service_status_label.config(text=service_status, foreground=service_color)
        self.vpn_status_label.config(text=vpn_status, foreground=vpn_color)
        self.network_status_label.config(text=network_status, foreground=network_color)

        # UPDATE PROCESS LIST
        self.processes_listbox.delete(0, tk.END)
        for process in vpn_processes:
            self.processes_listbox.insert(tk.END, f"{process['name']} (PID: {process['pid']})")

        # UPDATE LOG DISPLAY
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        for entry in log_entries:
            self.log_text.insert(tk.END, entry)
        self.log_text.config(state=tk.DISABLED)

    # ============================================================================
    # STATUS MONITORING INITIALIZATION
    # ============================================================================
    def start_status_monitoring(self) -> None:
        """
        Start periodic status updates in a background thread.
        """
        # STATUS MONITOR LOOP
        def status_monitor_loop() -> None:
            while True:
                self.update_status()
                time.sleep(2)
        threading.Thread(target=status_monitor_loop, daemon=True).start()


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================
def main() -> None:
    """
    Main function to initialize and run the VPN Kill Switch application.

    Creates the main Tkinter window, initializes the VPNKillSwitchConfigGUI class,
    and starts the application event loop.
    """
    # MAIN WINDOW CREATION
    root: tk.Tk = tk.Tk()

    # APPLICATION INITIALIZATION
    app: VPNKillSwitchConfigGUI = VPNKillSwitchConfigGUI(root)

    # APPLICATION EXECUTION
    # Start the application's main event loop
    root.mainloop()


# ============================================================================
# PROGRAM EXECUTION GUARD
# ============================================================================
if __name__ == "__main__":
    # Execute main function only when script is run directly
    main()
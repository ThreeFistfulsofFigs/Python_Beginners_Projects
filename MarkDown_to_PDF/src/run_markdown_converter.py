# ============================================================================
# MARKDOWN TO PDF CONVERTER LAUNCHER
# ============================================================================
# This script checks for required dependencies and launches the Markdown to PDF
# Converter application. It ensures all necessary packages are installed before
# starting the main application.
# ============================================================================

# Import required libraries
import time           # For delaying execution on error
import sys            # For modifying Python path
import os             # For path operations
sys.path.append(os.path.dirname(__file__))  # Ensure src/ is in Python path

# ============================================================================
# DEPENDENCY CHECK AND INSTALLATION
# ============================================================================
def check_and_install_dependencies():
    """
    Check if required Python packages are installed and install them if needed.

    Returns:
        bool: True if all dependencies are installed, False if installation fails
    """
    # REQUIRED PACKAGES
    # List of Python packages needed for the application
    required_packages = ['markdown2', 'pdfkit']
    missing_packages = []

    # CHECK INSTALLED PACKAGES
    # Verify each required package is available
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is already installed")
        except ImportError:
            missing_packages.append(package)

    # INSTALL MISSING PACKAGES
    # Attempt to install any missing packages using pip
    if missing_packages:
        print("\nMissing dependencies detected. Installing required packages...")
        for package in missing_packages:
            try:
                import pip
                pip.main(['install', package])
                print(f"✓ Successfully installed {package}")
            except Exception as e:
                print(f"✗ Failed to install {package}: {e}")
                return False

        print("\nAll dependencies installed successfully!")
        return True
    else:
        print("All dependencies are already installed.")
        return True

# ============================================================================
# MAIN PROGRAM LOGIC
# ============================================================================
def main():
    """
    Main function to check dependencies and launch the application.

    Returns:
        None: Launches the application or displays error message
    """
    try:
        # DEPENDENCY CHECK
        # Ensure all required packages are installed
        print("Checking dependencies...")
        if check_and_install_dependencies():
            # LAUNCH APPLICATION
            # Start the Markdown to PDF Converter
            print("\nStarting Markdown to PDF Converter...\n")
            from main import MarkdownConverterApp
            app = MarkdownConverterApp()
            app.run()
        else:
            # DEPENDENCY INSTALLATION FAILED
            # Inform user to install packages manually
            print("\nFailed to install required dependencies.")
            print("Please install the missing packages manually and try again.")
            time.sleep(5)
    except Exception as e:
        # ERROR HANDLING
        # Display error details and keep window open for user to read
        import traceback
        print(f"\nError launching application: {e}")
        traceback.print_exc()
        input("\nPress Enter to close this window...")

# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================
if __name__ == '__main__':
    # Execute main function only when script is run directly
    main()

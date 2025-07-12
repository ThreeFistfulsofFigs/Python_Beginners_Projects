# ==========================================================
# Build Configuration
# Description: Configures cx_Freeze to create an executable for the US States Quiz
# ==========================================================
from cx_Freeze import setup, Executable

# ==========================================================
# File Inclusions
# Description: Specifies additional files to include in the build
# ==========================================================
include_files = [
    "50_states.csv",
    "blank_states_img.gif"
]

# ==========================================================
# Build Options
# Description: Defines packages and optimization settings for the executable
# ==========================================================
build_exe_options = {
    "packages": ["tkinter", "pandas", "turtle", "csv", "os", "sys"],
    "include_files": include_files,
    "optimize": 0
}

# ==========================================================
# Setup Configuration
# Description: Sets up the executable with metadata and build options
# ==========================================================
setup(
    name="US States Quiz",
    version="1.0",
    description="Quiz o ameriških državah",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=None)]
)
# python setup.py build
# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                          Grok Image Generator                             ║
# ║  A GUI application to generate and display images using the Grok API      ║
# ║  Features:                                                                ║
# ║  - Prompt-based image generation with quick prompts                       ║
# ║  - Support for input images and real-time display                         ║
# ║  - Progress tracking and status logging                                   ║
# ║  - Threaded API calls for responsiveness                                  ║
# ║  Author: [Your Name]                                                     ║
# ║  Creation Date: July 22, 2025                                            ║
# ║  Last Modified: July 22, 2025                                            ║
# ║  Notes: Requires grok3api and Pillow; uses custom imghdr.py               ║
# ║         Future: Add export options or enhance UI responsiveness          ║
# ╚════════════════════════════════════════════════════════════════════════════╝

## Overview
The **Grok Image Generator** is a Python-based GUI application that allows users to create images using the Grok API from xAI. Users can input custom prompts or use predefined quick prompts, optionally upload an input image, and view generated images in a scrollable gallery. The app includes real-time status updates and error handling, making it a practical tool for exploring AI-generated imagery.

## Features
- **Prompt-Based Generation**: Enter custom prompts or select from quick prompts like "Create an image of a majestic sailing ship on stormy seas."
- **Input Image Support**: Optionally upload an image to influence the generated output.
- **Real-Time Display**: Generated images are displayed in a scrollable gallery within the GUI.
- **Progress Tracking**: A progress bar and detailed logs show the generation process.
- **Threaded Execution**: API calls run in a separate thread to keep the UI responsive.
- **Custom Compatibility**: Includes a custom `imghdr.py` for Python 3.13 compatibility.

## Getting Started

### Prerequisites
- **Python**: 3.7 or higher, installed and added to PATH.
  ```bash
  python --version
  ```
- **Dependencies**:
  - `Pillow>=8.0.0` for image processing.
  - `grok3api` for API integration (install via `pip install grok3api`).

### Installation
1. **Clone the Repository** (if not already part of the project):
   ```bash
   git clone https://github.com/ThreeFistfulsofFigs/Python_Beginners_Projects.git
   cd Python_Beginners_Projects/grok_image_generator
   ```
2. **Set Up Virtual Environment** (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```
3. **Install Dependencies**:
   ```bash
   pip install Pillow grok3api
   ```
4. **Place Files**:
   - Ensure `imghdr.py` and `main.py` are in the `grok_image_generator` directory.

### How to Use
1. **Run the Application**:
   ```bash
   python main.py
   ```
2. **Interact with the GUI**:
   - **Prompt Input**: Type a custom prompt (e.g., "Create an image of a futuristic city") or click a quick prompt button.
   - **Input Image**: Click "Browse" to select an optional input image (supported formats: PNG, JPG, JPEG, GIF, BMP, TIFF).
   - **Generate**: Click "🚀 Generate Image" to start the process.
   - **View Results**: Generated images appear in the "Generated Images" frame with an "Open" button to view files.
3. **Monitor Progress**:
   - Check the status text for logs (e.g., "🖼️ Found 1 generated image(s)!" or "❌ Error: ...").
   - The progress bar indicates ongoing tasks.

## Troubleshooting
- **GUI Not Displaying**:
  - Ensure `tkinter` is installed (`sudo apt-get install python3-tk` on Linux).
  - Verify Python is configured for graphical applications (e.g., a display server is running).
- **Module Not Found**:
  - Install missing dependencies (`pip install Pillow grok3api`).
  - Ensure the virtual environment is activated.
- **No Images Generated**:
  - Check the status text for "📝 No images were generated in the response" or "📄 Raw response: {...}".
  - Verify your Grok API credentials and account type (free or SuperGrok) for usage quotas.
  - Share the "📄 Raw response" log for further analysis.
- **Image Save Errors**:
  - Ensure write permissions in the project directory.
  - Check for "⚠️ Image object found but no save method available" in logs.
- **Slow Performance**:
  - API response times depend on your internet connection and Grok server load.

## Contributing
Contributions are welcome! To enhance the Grok Image Generator:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Modify `main.py` or add new files (e.g., for export functionality).
4. Commit changes: `git commit -m "Add your feature"`.
5. Push to your fork: `git push origin feature/your-feature`.
6. Open a pull request on the [GitHub repository](https://github.com/ThreeFistfulsofFigs/Python_Beginners_Projects).

## Notes
- **Version**: 1.0.0
- **License**: MIT (see repository LICENSE file).
- **Security**: Ensure Grok API keys are stored securely and not hardcoded in `main.py`.
- **Executable**: Can be converted to a standalone executable using PyInstaller (see repository README for details).

## Contact
For questions or suggestions, open an issue on the [GitHub repository](https://github.com/ThreeFistfulsofFigs/Python_Beginners_Projects) or contact via email: [gerrit.meurer952@dontsp.am](mailto:gerrit.meurer952@dontsp.am).
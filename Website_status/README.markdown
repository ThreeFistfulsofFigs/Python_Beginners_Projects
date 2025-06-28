# Website Status Checker

## Overview
The Website Status Checker is a Python command-line tool for monitoring website availability and performance. It analyzes HTTP responses, including status codes, headers, server information, and response times, with support for single or batch URL checks.

## Features
- **HTTP Analysis**: Reports status codes, response times, and server details.
- **Security Headers**: Checks presence of key security headers (e.g., HSTS, CSP).
- **Batch Processing**: Supports checking multiple URLs with summary.
- **Interactive Mode**: Allows manual URL input for real-time checks.
- **Error Handling**: Manages timeouts, connection issues, and invalid URLs.
- **Formatted Output**: Displays detailed results with visual indicators.

## Requirements
- **Operating System**: Any (Windows, macOS, Linux)
- **Python**: 3.7 or higher
- **Dependencies**:
  - `requests>=2.25.0`
  - Built-in: `time`, `urllib.parse`

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
3. **Install Dependencies**:
   ```bash
   pip install requests
   ```

### Step 2: Run the Script
1. **Locate Script**: Navigate to the project directory containing `main.py`.
2. **Run in Default Mode**:
   ```bash
   python main.py
   ```
   - Checks a sample URL (e.g., TradingView chart).
3. **Run in Interactive Mode**:
   - Uncomment `interactive_mode()` and comment `main()` in `main.py`.
   ```bash
   python main.py
   ```

## Usage

### Step 1: Check Website Status
1. **Default Mode**:
   - Runs check on sample URL and displays results (e.g., status code, response time, headers).
2. **Interactive Mode**:
   - Enter URLs manually (e.g., `https://example.com`).
   - Type `quit` to exit.
3. **Batch Mode**:
   - Modify `main.py` to call `check_multiple_urls([url_list])` with a list of URLs.

### Step 2: Verify Output
- **Sample Output**:
  ```
  URL: https://www.tradingview.com/...
  Status Code: 200 ✓ (Request successful)
  Response Time: 0.453 seconds
  Server: cloudflare
  Security Headers: 3/6 present
  ```
- **Log Verification**: Check console for errors or warnings (e.g., `✗ Connection error`).

### Step 3: Testing
1. **Test Valid URL**:
   - Run with a known URL (e.g., `https://example.com`) and verify success.
2. **Test Invalid URL**:
   - Input malformed URL (e.g., `invalid`) to confirm error handling.
3. **Test Batch Mode**:
   - Check multiple URLs and verify summary (e.g., `Successful checks: 2/3`).

## Configuration
- **Constants** (in `main.py`):
  ```python
  DEFAULT_TIMEOUT = 30  # Request timeout in seconds
  DEFAULT_USER_AGENT = "Website-Status-Checker/1.0"
  MAX_REDIRECTS = 5
  ```

## Troubleshooting

### "Request timeout" or "Connection error"
- Check internet connection.
- Increase `DEFAULT_TIMEOUT` in `main.py`.
- Verify URL is accessible.

### "Module not found"
- Install `requests`:
  ```bash
  pip install requests
  ```

## Files Included
- `main.py`: Core script with status checking logic.

## Notes
- **Version**: 1.0.0
- **Rate Limiting**: Includes 1-second pause in batch mode to avoid server overload.

## Support
For issues, check console output or submit an issue at [GitHub repository URL] (replace with your repo URL).
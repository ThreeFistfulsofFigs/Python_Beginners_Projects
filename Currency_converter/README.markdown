# Currency Converter

## Overview
The Currency Converter is a Python command-line tool that converts an amount from one currency to another using real-time exchange rates from the freecurrencyapi.com API. It includes a fallback to a local JSON file (`rates.json`) for offline use and robust input validation with retry logic for a seamless user experience. Ideal for travelers, businesses, or anyone needing accurate currency conversions.

## Features
- **Real-Time Conversion**: Fetches live exchange rates from freecurrencyapi.com.
- **Offline Fallback**: Uses `rates.json` if API is unavailable.
- **Input Validation**: Ensures valid amount and currency inputs with retry prompts.
- **Rate Caching**: Saves API-fetched rates to `rates.json` for future offline use.
- **Logging**: Outputs status messages to console for debugging.

## Requirements
- **Operating System**: Any (Windows, macOS, Linux)
- **Python**: 3.7 or higher
- **Dependencies**:
  - `requests>=2.25.0`
  - Built-in: `json`, `typing`
- **API Key**: Required for freecurrencyapi.com (insert into `main.py`).

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

### Step 2: Configure API Key
1. Sign up at [freecurrencyapi.com](https://freecurrencyapi.com) to obtain an API key.
2. Replace `"insert your API key here"` in `main.py` with the API URL containing your key (e.g., `https://api.freecurrencyapi.com/v1/latest?base_currency=EUR&apikey=YOUR_KEY`).

## Usage

### Step 1: Run the Script
1. **Locate Script**: Navigate to the project directory containing `main.py`.
2. **Run the Script**:
   ```bash
   python main.py
   ```
3. **Follow Prompts**:
   - Enter the amount to convert (e.g., `100`).
   - Enter the base currency (e.g., `EUR`).
   - Enter the target currency (e.g., `DKK`).
   - View the converted amount (e.g., `100.00 EUR = 745.50 DKK`).

### Step 2: Verify Functionality
- **API Success**: Confirms rates fetched from API or `rates.json`.
- **Error Handling**: Retries on invalid inputs (e.g., non-numeric amounts or unsupported currencies).
- **Offline Mode**: Uses `rates.json` if API fails (ensure file exists from prior API call).

### Step 3: Testing
1. **Test Conversion**:
   - Run with valid inputs (e.g., `100`, `EUR`, `USD`).
   - Verify output matches expected rates (based on API or `rates.json`).
2. **Test Offline Mode**:
   - Disconnect internet and run script to confirm fallback to `rates.json`.
   - Check console for messages like:
     ```
     Loaded rates from JSON: ['eur', 'usd', 'dkk', ...]
     100.00 EUR = 745.50 DKK
     ```
3. **Test Invalid Inputs**:
   - Enter non-numeric amount (e.g., `abc`) to verify retry prompt.
   - Enter unsupported currency (e.g., `XYZ`) to confirm error handling.

## Configuration
- **Config File**: `rates.json` (auto-generated after successful API call).
- **Default Settings**:
  ```json
  {
      "eur": {"rate": 1.0},
      "usd": {"rate": 1.12},
      "dkk": {"rate": 7.455},
      ...
  }
  ```

## Troubleshooting

### "API request failed"
- Verify API key in `main.py` is correct.
- Check internet connection.
- Ensure `rates.json` exists for offline fallback.

### "Invalid JSON format in rates file"
- Delete corrupted `rates.json` and run script with internet to regenerate.
- Verify file permissions in the project directory.

### "Module not found" Errors
- Install missing modules:
  ```bash
  pip install requests
  ```
- Ensure Python 3.7+ is used: `python --version`.

## Files Included
- `main.py`: Core script with conversion logic and API/JSON handling.
- `rates.json` (optional): Generated file for offline rate storage.

## Notes
- **Version**: 1.0.0
- **API Dependency**: Requires a valid freecurrencyapi.com API key.
- **Security**: Store API key securely; avoid sharing `main.py` with key included.

## Support
For issues, check console output or submit an issue at [GitHub repository URL] (replace with your repo URL).
Currency Converter
A Python-based tool that converts amounts between currencies using real-time exchange rates from the freecurrencyapi.com API. If the API is unavailable, it falls back to a local JSON file (rates.json). After each successful API call, rates are saved to the JSON file for offline use. The program includes input validation and retry logic for a seamless user experience.
Features

Converts amounts between supported currencies (e.g., EUR to USD, DKK to JPY).
Fetches real-time exchange rates from freecurrencyapi.com with a JSON fallback.
Saves API-fetched rates to a local file for offline conversions.
Validates user inputs with retry prompts for amount and currency codes.
Displays results with two decimal places.

Technologies Used

Python 3.x
requests (for API calls)
json (for file handling)
Type hints via typing for better code clarity

Requirements

Python 3.x installed
requests package:pip install requests


freecurrencyapi.com API key (replace "insert your API key here" in main.py)
rates.json file with initial exchange rates (included)

Installation

Install the required Python package:pip install requests


Obtain an API key from freecurrencyapi.com and replace the placeholder in main.py.
Save the rates.json file in the same directory as main.py.
Clone or copy the main.py script to your project directory.

Usage

Run the script:python main.py


Enter the amount to convert (e.g., 100).
Enter the base currency (e.g., EUR) from the listed options.
Enter the target currency (e.g., USD) from the listed options.
View the conversion result (e.g., 100.00 EUR = 116.89 USD).

Notes

The script attempts to fetch rates from the API first; if it fails (e.g., due to network issues), it uses rates.json.
A 5-second timeout is set for API requests to prevent hangs.
Supported currencies are listed when prompted (e.g., AUD, BGN, USD, etc., from rates.json).
Ensure the API key is valid, or the fallback to rates.json will be triggered.

Limitations

Requires an internet connection for initial API calls unless rates.json is pre-populated.
No persistent storage for conversion history.
API rate limits may apply depending on the freecurrencyapi.com plan.

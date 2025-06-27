# ============================================================================
# CURRENCY CONVERTER
# ============================================================================
# This script converts an amount from one currency to another using real-time
# exchange rates fetched from the freecurrencyapi.com API. If the API is
# unavailable, it falls back to a local JSON file (rates.json). After each
# successful API call, rates are saved to the JSON file for future offline use.
# The program includes robust input validation with retry logic for user inputs,
# ensuring a seamless experience for travelers, businesses, or anyone needing
# accurate currency conversions.
# ============================================================================

# Import required libraries
import json  # For reading and writing JSON files
import requests  # For making API requests to fetch exchange rates
from typing import Dict, Tuple  # For type hints in function signatures


# ============================================================================
# JSON HANDLING FUNCTIONS
# ============================================================================

def load_rates(json_file: str = "rates.json") -> Dict[str, dict]:
    """
    Load exchange rates from a JSON file as a backup when API is unavailable.

    Args:
        json_file (str): Path to the JSON file containing exchange rates (default: "rates.json").

    Returns:
        Dict[str, dict]: Dictionary of currency codes to their exchange rates (relative to EUR).

    Raises:
        FileNotFoundError: If the JSON file is not found.
        ValueError: If the JSON file is invalid or missing the 'eur' currency.
        KeyError: If the JSON file has an invalid structure.
    """
    try:
        # FILE READING
        # Open and read the JSON file containing exchange rates
        with open(json_file, 'r') as file:
            rates = json.load(file)

        # DEBUG OUTPUT
        # Display loaded currencies for verification
        print(f"Loaded rates from JSON: {list(rates.keys())}")

        # EUR VALIDATION
        # Ensure 'eur' is present, as it's critical for conversion logic
        if "eur" not in rates:
            raise ValueError("Error: JSON file missing 'eur' currency.")

        return rates

    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file {json_file} was not found.")
    except json.JSONDecodeError:
        raise ValueError("Error: Invalid JSON format in rates file.")
    except KeyError:
        raise ValueError("Error: JSON file has invalid structure.")


def save_rates(rates: Dict[str, dict], json_file: str = "rates.json") -> None:
    """
    Save exchange rates to a JSON file for future offline use.

    Args:
        rates (Dict[str, dict]): Dictionary of currency codes and their exchange rates.
        json_file (str): Path to the JSON file to save rates (default: "rates.json").

    Raises:
        IOError: If the file cannot be written.
    """
    try:
        # FILE WRITING
        # Save rates to JSON with readable formatting
        with open(json_file, 'w') as file:
            json.dump(rates, file, indent=4)
        print(f"Saved rates to {json_file}")

    except IOError as e:
        # ERROR FEEDBACK
        # Inform user of failure to save file
        print(f"Error: Failed to save rates to {json_file}: {str(e)}")


# ============================================================================
# API FETCHING FUNCTION
# ============================================================================

def get_api_rates() -> Dict[str, dict]:
    """
    Fetch exchange rates from freecurrencyapi.com API and save to JSON.

    Returns:
        Dict[str, dict]: Dictionary of currency codes to their exchange rates (relative to EUR).

    Raises:
        ConnectionError: If the API request fails (e.g., network issues).
        ValueError: If the API response is invalid or missing 'eur'.
    """
    # API CONFIGURATION
    # Use provided API URL with EUR as base currency
    url = "insert your API key here"

    try:
        # API REQUEST
        # Fetch data with a timeout to prevent hanging
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        # RESPONSE VALIDATION
        # Ensure the response contains valid rate data
        if "data" not in data:
            raise ValueError(f"API request failed: {data.get('message', 'Invalid response')}")

        # DATA TRANSFORMATION
        # Convert API response to match expected format: {currency: {"rate": value}}
        rates = {
            currency.lower(): {"rate": rate}
            for currency, rate in data["data"].items()
        }

        # DEBUG OUTPUT
        # Display loaded currencies for verification
        print(f"Loaded rates from API: {list(rates.keys())}")

        # EUR VALIDATION
        # Ensure 'eur' is present for conversion logic
        if "eur" not in rates:
            raise ValueError("Error: API response missing 'eur' currency.")

        # SAVE RATES
        # Store fetched rates to JSON for backup
        save_rates(rates)

        return rates

    except requests.RequestException as e:
        raise ConnectionError(f"Error fetching API data: {str(e)}")


# ============================================================================
# CORE CONVERSION FUNCTION
# ============================================================================

def convert(amount: float, base: str, to: str, rates: Dict[str, dict]) -> float:
    """
    Convert an amount from one currency to another using provided exchange rates.

    Args:
        amount (float): The amount to convert.
        base (str): The source currency code (e.g., "EUR").
        to (str): The target currency code (e.g., "DKK").
        rates (Dict[str, dict]): Dictionary of currency codes and their exchange rates.

    Returns:
        float: The converted amount in the target currency.

    Raises:
        ValueError: If either currency is not supported in the rates dictionary.
    """
    # CASE NORMALIZATION
    # Convert currency codes to lowercase for consistency
    base = base.lower()
    to = to.lower()

    # CURRENCY VALIDATION
    # Ensure both currencies exist in rates
    from_rates = rates.get(base)
    to_rates = rates.get(to)
    if not from_rates:
        raise ValueError(f"Currency {base} not supported.")
    if not to_rates:
        raise ValueError(f"Currency {to} not supported.")

    # CONVERSION CALCULATION
    # Convert to EUR first (amount / base_rate), then to target (result * to_rate)
    amount_in_eur = amount / from_rates["rate"]
    return amount_in_eur * to_rates["rate"]


# ============================================================================
# USER INPUT FUNCTION
# ============================================================================

def get_user_input(rates: Dict[str, dict]) -> Tuple[float, str, str]:
    """
    Get and validate user input for amount and currencies with retry logic.

    Args:
        rates (Dict[str, dict]): Dictionary of currency codes and their exchange rates.

    Returns:
        Tuple[float, str, str]: Tuple containing the amount, base currency, and target currency.

    Raises:
        None: Invalid inputs are handled with retry prompts instead of raising errors.
    """
    # AMOUNT INPUT LOOP
    # Continue until a valid positive number is entered
    while True:
        try:
            amount_input = input("Enter amount to convert (positive number): ").strip()
            amount = float(amount_input)
            if amount <= 0:
                print("Error: Amount must be positive. Please try again.")
                continue
            break
        except ValueError:
            print("Error: Amount must be a valid number. Please try again.")

    # BASE CURRENCY INPUT LOOP
    # Continue until a supported base currency is entered
    while True:
        print("Available currencies:", ", ".join(sorted(rates.keys())))
        base = input("Enter base currency (e.g., EUR): ").strip().lower()
        if base not in rates:
            print(f"Error: Base currency {base} not supported. Please try again.")
            continue
        break

    # TARGET CURRENCY INPUT LOOP
    # Continue until a supported target currency is entered
    while True:
        to = input("Enter target currency (e.g., DKK): ").strip().lower()
        if to not in rates:
            print(f"Error: Target currency {to} not supported. Please try again.")
            continue
        break

    return amount, base, to


# ============================================================================
# MAIN PROGRAM LOGIC
# ============================================================================

def main() -> None:
    """
    Main function to handle currency conversion with API and JSON fallback.

    Fetches exchange rates from an API (default) or JSON file (backup), collects
    user input, and performs the conversion. Saves API rates to JSON for future use.
    """
    # RATE FETCHING
    # Attempt to load rates, prioritizing API
    rates = None
    try:
        # API ATTEMPT
        # Fetch rates from freecurrencyapi.com
        print("Attempting to fetch rates from API...")
        rates = get_api_rates()
        print("Using rates from API.")
    except Exception as api_e:
        # API FAILURE HANDLING
        # Fall back to JSON if API fails
        print(f"API error: {api_e}")
        try:
            print("Falling back to JSON file...")
            rates = load_rates("rates.json")
            print("Using rates from JSON file.")
        except (FileNotFoundError, ValueError) as e:
            print(f"Failed to load JSON rates: {e}")
            return

    # RATE VALIDATION
    # Ensure rates were loaded successfully
    if not rates:
        print("Error: No rates loaded. Cannot proceed with conversion.")
        return

    # USER INPUT AND CONVERSION
    # Collect input and perform conversion
    try:
        # INPUT COLLECTION
        # Get validated amount and currencies
        amount, base, to = get_user_input(rates)

        # CONVERSION EXECUTION
        # Calculate the converted amount
        result = convert(amount, base, to, rates)

        # RESULT DISPLAY
        # Show the conversion result with 2 decimal places
        print(f"\n{amount:.2f} {base.upper()} = {result:.2f} {to.upper()}")

    except Exception as e:
        # ERROR FEEDBACK
        # Handle any unexpected errors during conversion
        print(f"Unexpected error: {str(e)}")


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Execute main function only when script is run directly
    main()


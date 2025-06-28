Expense Splitting Calculator
A Python-based tool that calculates how to split expenses among multiple people using custom percentage contributions. Ideal for shared bills, group trips, or any scenario requiring proportional expense division, with support for locale-specific currency formatting.
Features

Splits total expenses based on user-defined percentages for each person.
Validates that percentages sum to 100% with retry logic.
Formats currency output with thousands separators and two decimal places (e.g., €1,234.56) using the system locale.
Provides a detailed breakdown of each person’s share.
Includes comprehensive input validation for amounts and number of people.

Technologies Used

Python 3.x
locale (included with Python) for currency formatting

Requirements

Python 3.x installed
System locale set to a supported format (e.g., en_US.UTF-8 for comma-separated thousands)

Installation

Clone or copy the main.py script to your project directory.
No additional packages are required.

Usage

Run the script:python main.py


Enter the total amount of expenses (e.g., 1234.56).
Enter the number of people (e.g., 3).
For each person, enter their percentage contribution (e.g., 40, 30, 30—must sum to 100%).
View the calculated split for each person.

Notes

The default currency symbol is € but can be adjusted by modifying the currency parameter in calculate_split.
Uses the en_US.UTF-8 locale for formatting; change locale.setlocale if needed for other regions.
Retries input if percentages don’t sum to 100% or if invalid numbers are entered.

Limitations

No persistent storage for past calculations.
Currency symbol and locale are hardcoded; customization requires code modification.
Assumes all inputs are numeric; non-numeric input triggers a retry.

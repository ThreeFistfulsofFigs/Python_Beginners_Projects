Personal Finance Calculator
A Python-based tool that calculates personal financial information, including taxes, net income, and available funds after expenses. It provides detailed monthly and yearly breakdowns with proper currency formatting, making it useful for budgeting and financial planning.
Features

Calculates monthly and yearly taxes based on a user-defined tax rate.
Determines net income after tax deductions for both monthly and yearly periods.
Computes available funds after subtracting monthly expenses from net income.
Formats output with thousands separators and two decimal places (e.g., €1,234.56) using the system locale.
Includes input validation to ensure all values are numeric.

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


Enter your gross monthly income (e.g., 5000).
Enter the tax rate as a percentage (e.g., 25.5 for 25.5%).
Enter your total monthly expenses (e.g., 2000 for rent, food, etc.).
View the detailed financial summary, including monthly and yearly figures.

Notes

The default currency symbol is € (with a space), but it can be changed by modifying the currency parameter in calculate_finances.
Uses the en_US.UTF-8 locale for formatting; adjust locale.setlocale if needed for other regions.
Available funds can be negative if expenses exceed net income, indicating a budget deficit.

Limitations

No persistent storage for past calculations.
Currency symbol and locale are hardcoded; customization requires code modification.
Assumes consistent monthly income and expenses over 12 months.

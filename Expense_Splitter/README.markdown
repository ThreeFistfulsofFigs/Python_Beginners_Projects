# Expense Splitting Calculator

## Overview
The Expense Splitting Calculator is a Python command-line tool that splits expenses among multiple people based on custom percentage contributions. It ensures percentages sum to 100% and provides formatted output with proper currency formatting. Perfect for shared bills, group trips, or proportional expense division.

## Features
- **Custom Splits**: Assigns percentages to each person for unequal splits.
- **Input Validation**: Ensures valid inputs and 100% total percentage.
- **Currency Formatting**: Displays amounts with locale-based formatting (e.g., €1,234.56).
- **Console Output**: Shows clear breakdown of each person’s share.

## Requirements
- **Operating System**: Any (Windows, macOS, Linux)
- **Python**: 3.7 or higher
- **Dependencies**: Built-in `locale` module

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

### Step 2: Run the Script
1. **Locate Script**: Navigate to the project directory containing `main.py`.
2. **Run the Script**:
   ```bash
   python main.py
   ```

## Usage

### Step 1: Split Expenses
1. **Enter Total Amount**: Input the total expense (e.g., `1000`).
2. **Enter Number of People**: Specify how many people are splitting (e.g., `3`).
3. **Enter Percentages**: Provide each person’s percentage (e.g., `50`, `30`, `20`).
4. **View Results**:
   - Output shows total amount and each person’s share (e.g., `Person 1: 50.00% = €500.00`).

### Step 2: Testing
1. **Test Valid Inputs**:
   - Input: Total=`1000`, People=`3`, Percentages=`40, 30, 30`.
   - Verify output:
     ```
     Total expenses: €1,000.00
     Number of people: 3
     Person 1: 40.00% = €400.00
     Person 2: 30.00% = €300.00
     Person 3: 30.00% = €300.00
     ```
2. **Test Invalid Inputs**:
   - Enter non-numeric amount (e.g., `abc`) to confirm retry prompt.
   - Enter percentages summing to != 100% (e.g., `50, 50, 50`) to verify error handling.

## Configuration
- **Currency**: Hardcoded to `€` in `main.py` (modify `currency` parameter in `calculate_split` for other symbols).
- **Locale**: Uses `en_US.UTF-8` for formatting (modify `locale.setlocale` for other locales).

## Troubleshooting

### "Please enter a valid number"
- Ensure inputs are numeric (e.g., `1000`, not `1,000` or `abc`).
- Verify percentages are between 0 and 100.

### Locale Issues
- If formatting is incorrect, verify system locale or modify `locale.setlocale` in `main.py`.

## Files Included
- `main.py`: Core script with expense splitting logic.

## Notes
- **Version**: 1.0.0
- **Locale**: Defaults to US English formatting; adjust for other regions if needed.

## Support
For issues, check console output or submit an issue at [GitHub repository URL] (replace with your repo URL).
# Personal Finance Calculator

## Overview
The Personal Finance Calculator is a Python command-line tool that calculates net income, taxes, and available funds after expenses. It provides monthly and yearly financial breakdowns with proper currency formatting, ideal for personal budgeting and financial planning.

## Features
- **Financial Breakdown**: Calculates monthly/yearly taxes, net income, and discretionary funds.
- **Input Validation**: Ensures valid numeric inputs with retry prompts.
- **Currency Formatting**: Uses locale-based formatting (e.g., €1,234.56).
- **Console Output**: Displays clear financial summary.

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

### Step 1: Calculate Finances
1. **Enter Monthly Income**: Input gross monthly income (e.g., `5000`).
2. **Enter Tax Rate**: Input tax rate as percentage (e.g., `25`).
3. **Enter Monthly Expenses**: Input total expenses (e.g., `3000`).
4. **View Results**:
   - Output shows monthly and yearly breakdowns:
     ```
     Monthly Income: €5,000.00
     Tax rate: 25.00%
     Monthly Tax: €1,250.00
     Monthly Net Income: €3,750.00
     Yearly Salary: €60,000.00
     Yearly Tax: €15,000.00
     Yearly Net Income: €45,000.00
     Monthly Available Finances After Expenses: €750.00
     ```

### Step 2: Testing
1. **Test Valid Inputs**:
   - Input: Income=`5000`, Tax=`25`, Expenses=`3000`.
   - Verify output matches expected calculations.
2. **Test Invalid Inputs**:
   - Enter non-numeric input (e.g., `abc`) to confirm retry prompt.

## Configuration
- **Currency**: Hardcoded to `€` in `main.py` (modify `currency` parameter in `calculate_finances`).
- **Locale**: Uses `en_US.UTF-8` for formatting (modify `locale.setlocale` for other locales).

## Troubleshooting

### "Please enter a valid number"
- Ensure inputs are numeric (e.g., `5000`, not `5,000` or `abc`).

### Locale Issues
- If formatting is incorrect, verify system locale or modify `locale.setlocale` in `main.py`.

## Files Included
- `main.py`: Core script with financial calculation logic.

## Notes
- **Version**: 1.0.0
- **Locale**: Defaults to US English formatting; adjust for other regions if needed.

## Support
For issues, check console output or submit an issue at [GitHub repository URL] (replace with your repo URL).
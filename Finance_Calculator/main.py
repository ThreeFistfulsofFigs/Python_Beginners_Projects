# ============================================================================
# PERSONAL FINANCE CALCULATOR
# ============================================================================
# This script calculates personal financial information including taxes,
# net income, and available funds after expenses. It provides both monthly
# and yearly breakdowns with proper currency formatting.
# ============================================================================

# Import required libraries
import locale  # For number and currency formatting based on system locale

# ============================================================================
# LOCALE CONFIGURATION
# ============================================================================
# Set locale for currency formatting (e.g., for Euro, adjust based on your system)
# This ensures numbers are displayed with proper thousands separators and decimal points
# according to the specified locale (US English format in this case)
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


# ============================================================================
# CORE FINANCIAL CALCULATION FUNCTION
# ============================================================================
def calculate_finances(monthly_income: float, tax_rate: float, expenses: float, currency: str) -> None:
    """
    Calculates and displays comprehensive financial information including taxes,
    net income, and available funds after expenses for both monthly and yearly periods.

    Args:
        monthly_income (float): Gross monthly income before taxes
        tax_rate (float): Tax rate as a percentage (e.g., 25.5 for 25.5%)
        expenses (float): Total monthly expenses (rent, food, utilities, etc.)
        currency (str): Currency symbol to display (e.g., '€ ', '$ ')

    Returns:
        None: Prints formatted financial summary to console
    """

    # MONTHLY TAX CALCULATIONS
    # Calculate how much tax is owed each month
    # Convert percentage to decimal by dividing by 100, then multiply by income
    monthly_tax: float = monthly_income * (tax_rate / 100)

    # MONTHLY NET INCOME CALCULATION
    # Determine take-home pay after tax deduction
    # This is the actual amount available to spend each month
    monthly_net_income: float = monthly_income - monthly_tax

    # YEARLY SALARY CALCULATIONS
    # Calculate total gross income for the entire year
    # Assumes 12 months of consistent income
    yearly_salary: float = monthly_income * 12

    # YEARLY TAX CALCULATIONS
    # Calculate total tax burden for the entire year
    # Simply multiply monthly tax by 12 months
    yearly_tax: float = monthly_tax * 12

    # YEARLY NET INCOME CALCULATION
    # Determine total take-home pay for the year
    # Alternative calculation: yearly_net_income = monthly_net_income * 12
    yearly_net_income: float = yearly_salary - yearly_tax

    # AVAILABLE FUNDS CALCULATION
    # Calculate remaining money after essential expenses
    # This represents discretionary income for savings, entertainment, etc.
    after_expenses: float = monthly_net_income - expenses

    # ========================================================================
    # FORMATTED OUTPUT DISPLAY
    # ========================================================================

    # VISUAL SEPARATOR
    # Create clear visual boundary for the financial report
    print('____________________________________')

    # INCOME INFORMATION
    # Display gross monthly income with proper currency formatting
    # :,.2f format adds thousands separators and 2 decimal places
    print(f'Monthly Income: {currency}{monthly_income:,.2f}')

    # TAX RATE DISPLAY
    # Show the tax rate as entered by user with 2 decimal precision
    print(f'Tax rate: {tax_rate:0.2f}%')

    # MONTHLY TAX AMOUNT
    # Display calculated monthly tax burden
    print(f'Monthly Tax: {currency}{monthly_tax:,.2f}')

    # MONTHLY NET INCOME
    # Show take-home pay after tax deduction
    print(f'Monthly Net Income: {currency}{monthly_net_income:,.2f}')

    # YEARLY FINANCIAL SUMMARY
    # Display annual financial figures for long-term planning
    print(f'Yearly Salary: {currency}{yearly_salary:,.2f}')
    print(f'Yearly Tax: {currency}{yearly_tax:,.2f}')
    print(f'Yearly Net Income: {currency}{yearly_net_income:,.2f}')

    # AVAILABLE FUNDS AFTER EXPENSES
    # Show discretionary income available for savings/entertainment
    # This can be negative if expenses exceed net income (budget deficit)
    print(f'Monthly Available Finances After Expenses: {currency}{after_expenses:,.2f}')

    # CLOSING VISUAL SEPARATOR
    print('____________________________________')


# ============================================================================
# MAIN PROGRAM LOGIC WITH INPUT VALIDATION
# ============================================================================
def main() -> None:
    """
    Main function that handles user input, validates data, and coordinates
    the financial calculation process. Includes error handling for invalid inputs.
    """

    # INPUT VALIDATION LOOP
    # Continue requesting input until all values are valid numbers
    # This prevents the program from crashing on invalid input
    while True:
        try:
            # USER INPUT COLLECTION
            # Get financial data from user with clear prompts

            # MONTHLY INCOME INPUT
            # Request gross monthly income before any deductions
            monthly_income = float(input('Please enter the monthly income: '))

            # TAX RATE INPUT
            # Request tax rate as a percentage (user enters 25, not 0.25)
            tax_rate = float(input('Please enter the tax rate (%): '))

            # MONTHLY EXPENSES INPUT
            # Request total monthly expenses (all categories combined)
            # Examples help user understand what to include
            expenses = float(input('Please enter the monthly expenses (e.g., rent, food, activities): '))

            # FINANCIAL CALCULATION EXECUTION
            # Call calculation function with user-provided data
            # Euro symbol is hardcoded but could be made configurable
            calculate_finances(monthly_income, tax_rate, expenses, currency='€ ')

            # SUCCESSFUL COMPLETION
            # Break out of input loop after successful calculation
            break

        # ERROR HANDLING
        # Catch conversion errors when user enters non-numeric values
        except ValueError as e:
            # USER-FRIENDLY ERROR MESSAGE
            # Don't show technical error details, just ask for valid input
            # This keeps the user experience clean and non-intimidating
            print(f"Please enter a valid number.")
            # Loop continues, asking for input again


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================
if __name__ == '__main__':
    # Execute main function only when script is run directly
    # (not when imported as a module)
    # This is a Python best practice for executable scripts
    main()
import locale

# Set locale for currency formatting (e.g., for Euro, adjust based on your system)
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # Configures the locale for currency and number formatting

def calculate_finances(monthly_income: float, tax_rate: float, expenses: float, currency: str) -> None:
    # Calculates monthly tax based on income and tax rate
    monthly_tax: float = monthly_income * (tax_rate / 100)
    # Computes net income after deducting monthly tax
    monthly_net_income: float = monthly_income - monthly_tax
    # Calculates yearly salary by multiplying monthly income by 12
    yearly_salary: float = monthly_income * 12
    # Computes yearly tax by multiplying monthly tax by 12
    yearly_tax: float = monthly_tax * 12
    # Calculates yearly net income by subtracting yearly tax from yearly salary
    yearly_net_income: float = yearly_salary - yearly_tax
    # Determines remaining finances after monthly expenses
    after_expenses: float = monthly_net_income - expenses

    # Prints a separator line for readability
    print('____________________________________')
    # Displays formatted monthly income with currency symbol
    print(f'Monthly Income: {currency}{monthly_income:,.2f}')
    # Shows the applied tax rate as a percentage
    print(f'Tax rate: {tax_rate:0.2f}%')
    # Displays calculated monthly tax with currency symbol
    print(f'Monthly Tax: {currency}{monthly_tax:,.2f}')
    # Shows net income after tax for the month
    print(f'Monthly Net Income: {currency}{monthly_net_income:,.2f}')
    # Displays total yearly salary
    print(f'Yearly Salary: {currency}{yearly_salary:,.2f}')
    # Shows total yearly tax
    print(f'Yearly Tax: {currency}{yearly_tax:,.2f}')
    # Displays net income for the year
    print(f'Yearly Net Income: {currency}{yearly_net_income:,.2f}')
    # Shows remaining finances after monthly expenses
    print(f'Monthly Available Finances After Expenses: {currency}{after_expenses:,.2f}')
    # Prints a closing separator line
    print('____________________________________')

def main() -> None:
    # Main loop to handle user input and calculation until valid data is provided
    while True:
        try:
            # Prompts user for monthly income and converts to float
            monthly_income = float(input('Please enter the monthly income: '))
            # Prompts user for tax rate and converts to float
            tax_rate = float(input('Please enter the tax rate (%): '))
            # Prompts user for monthly expenses and converts to float
            expenses = float(input('Please enter the monthly expenses (e.g., rent, food, activities): '))

            # Calls the finance calculation function with user inputs
            calculate_finances(monthly_income, tax_rate, expenses, currency='€ ')
            break  # Exits loop after successful calculation
        except ValueError as e:
            # Handles invalid input (non-numeric values) and prints error message
            print(f"Please enter a valid number. {str(e)}")

if __name__ == '__main__':
    # Executes the main function when the script is run directly
    main()


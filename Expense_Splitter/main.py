import locale

# Set locale for currency formatting (e.g., for Euro, adjust based on your system)
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # Configures the locale for currency and number formatting


def calculate_split(total_amount: float, number_of_people: int, currency: str = "€") -> None:
    """
    Calculates the split of total expenses based on user-provided percentages for each person.

    Args:
        total_amount (float): The total amount of expenses.
        number_of_people (int): The number of people to split the expenses among.
        currency (str): The currency symbol to use (default: "€").

    Raises:
        ValueError: If the number of people is less than or equal to 1, or if percentages don't sum to 100%.
    """
    # Validates that the number of people is greater than 1
    if number_of_people <= 1:
        raise ValueError("Number of people must be greater than 1.")

    # Loop to collect percentages until they sum to 100%
    while True:
        percentages = []  # Initializes list to store percentages for each person
        print(f"\nEnter the percentage split for each of the {number_of_people} people (total must be 100%):")
        # Collects percentage input for each person
        for i in range(number_of_people):
            while True:
                try:
                    percent = float(input(f"Percentage for person {i + 1} (0-100): "))
                    # Ensures percentage is within valid range
                    if percent < 0 or percent > 100:
                        raise ValueError("Percentage must be between 0 and 100.")
                    percentages.append(percent)  # Adds valid percentage to list
                    break
                except ValueError as e:
                    # Handles invalid percentage input with appropriate message
                    print(f"Please enter a valid number. {str(e)}")

        # Validates that the sum of percentages is approximately 100%
        total_percent = sum(percentages)
        if abs(total_percent - 100) <= 0.01:  # Allows small floating-point tolerance
            break
        else:
            # Prompts re-entry if percentages do not sum to 100%
            print(f"Error: Percentages sum to {total_percent:.2f}%, must be 100%. Please re-enter splits.")

    # Calculates the amount each person owes based on their percentage
    amounts = [total_amount * (p / 100) for p in percentages]

    # Displays the total expenses and individual splits
    print(f"\nTotal expenses: {currency}{total_amount:,.2f}")
    print(f"Number of people: {number_of_people}")
    for i, (percent, amount) in enumerate(zip(percentages, amounts), 1):
        # Prints the percentage and corresponding amount for each person
        print(f"Person {i}: {percent:.2f}% = {currency}{amount:,.2f}")


def main() -> None:
    """
    Main function to handle user input and run the expense splitting calculation.
    """
    while True:
        try:
            # Prompts user for the total amount of expenses and converts to float
            total_amount: float = float(input("Please enter the total amount of your expenses: "))
            if total_amount <= 0:
                raise ValueError("Total amount must be positive.")

            # Prompts user for the number of people and converts to int
            number_of_people: int = int(input("Please enter the number of people: "))
            if number_of_people <= 0:
                raise ValueError("Number of people must be positive.")

            # Calls the calculation function with user inputs
            calculate_split(total_amount, number_of_people)
            break  # Exits loop after successful calculation

        except ValueError as e:
            # Handles invalid input with detailed error message
            print(f"Please enter a valid number. {str(e)}")


if __name__ == "__main__":
    # Executes the main function when the script is run directly
    main()
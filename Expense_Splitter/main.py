# ============================================================================
# EXPENSE SPLITTING CALCULATOR
# ============================================================================
# This script calculates how to split expenses among multiple people based on
# custom percentage contributions. Perfect for shared bills, group trips,
# or any situation where expenses need to be divided proportionally.
# ============================================================================

# Import required libraries
import locale  # For number and currency formatting based on system locale

# ============================================================================
# LOCALE CONFIGURATION
# ============================================================================
# Set locale for currency formatting (e.g., for Euro, adjust based on your system)
# This ensures numbers are displayed with proper thousands separators and decimal points
# according to the specified locale (US English format provides comma separators)
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


# ============================================================================
# CORE EXPENSE SPLITTING FUNCTION
# ============================================================================
def calculate_split(total_amount: float, number_of_people: int, currency: str = "€") -> None:
    """
    Calculates the split of total expenses based on user-provided percentages for each person.
    This allows for unequal splits based on income, usage, or agreed-upon arrangements.

    Args:
        total_amount (float): The total amount of expenses to be split.
        number_of_people (int): The number of people to split the expenses among.
        currency (str): The currency symbol to use for display (default: "€").

    Raises:
        ValueError: If the number of people is less than or equal to 1, or if percentages don't sum to 100%.
    """

    # INPUT VALIDATION
    # Ensure we have at least 2 people (splitting among 1 person doesn't make sense)
    if number_of_people <= 1:
        raise ValueError("Number of people must be greater than 1.")

    # ========================================================================
    # PERCENTAGE COLLECTION WITH VALIDATION
    # ========================================================================

    # PERCENTAGE VALIDATION LOOP
    # Continue collecting percentages until they sum to exactly 100%
    # This ensures the entire expense amount is accounted for
    while True:
        # PERCENTAGE STORAGE
        percentages = []  # Initialize fresh list for each attempt

        # USER INSTRUCTION
        print(f"\nEnter the percentage split for each of the {number_of_people} people (total must be 100%):")

        # INDIVIDUAL PERCENTAGE COLLECTION
        # Get percentage for each person with validation
        for i in range(number_of_people):
            # SINGLE PERSON PERCENTAGE VALIDATION LOOP
            while True:
                try:
                    # PERCENTAGE INPUT
                    # Prompt for percentage with clear numbering (1-based for user friendliness)
                    percent = float(input(f"Percentage for person {i + 1} (0-100): "))

                    # RANGE VALIDATION
                    # Ensure percentage is within logical bounds
                    # Negative percentages don't make sense for expense splitting
                    # Percentages over 100% would mean paying more than the total
                    if percent < 0 or percent > 100:
                        raise ValueError("Percentage must be between 0 and 100.")

                    # VALID PERCENTAGE STORAGE
                    percentages.append(percent)
                    break  # Exit inner loop for this person

                except ValueError as e:
                    # INVALID INPUT HANDLING
                    # Handle both conversion errors and range errors
                    print(f"Please enter a valid number. {str(e)}")

        # ====================================================================
        # TOTAL PERCENTAGE VALIDATION
        # ====================================================================

        # SUM CALCULATION
        # Calculate total of all entered percentages
        total_percent = sum(percentages)

        # FLOATING-POINT TOLERANCE CHECK
        # Allow small rounding errors (0.01%) due to floating-point arithmetic
        # This prevents issues when users enter values like 33.33, 33.33, 33.34
        if abs(total_percent - 100) <= 0.01:
            break  # Exit percentage collection loop - we have valid data
        else:
            # RETRY PROMPT
            # Clear feedback about why the input was rejected
            print(f"Error: Percentages sum to {total_percent:.2f}%, must be 100%. Please re-enter splits.")
            # Loop continues, asking for all percentages again

    # ========================================================================
    # AMOUNT CALCULATION
    # ========================================================================

    # INDIVIDUAL AMOUNT CALCULATION
    # Calculate each person's share using list comprehension
    # Convert percentage to decimal (divide by 100) and multiply by total
    amounts = [total_amount * (p / 100) for p in percentages]

    # ========================================================================
    # FORMATTED RESULTS DISPLAY
    # ========================================================================

    # SUMMARY HEADER
    # Display the total amount being split
    print(f"\nTotal expenses: {currency}{total_amount:,.2f}")
    print(f"Number of people: {number_of_people}")

    # INDIVIDUAL BREAKDOWN
    # Show each person's percentage and corresponding dollar amount
    # enumerate with start=1 provides user-friendly numbering
    for i, (percent, amount) in enumerate(zip(percentages, amounts), 1):
        # DETAILED PERSON BREAKDOWN
        # Show both percentage and calculated amount for transparency
        # :,.2f format adds thousands separators and 2 decimal places
        print(f"Person {i}: {percent:.2f}% = {currency}{amount:,.2f}")


# ============================================================================
# MAIN PROGRAM LOGIC WITH COMPREHENSIVE INPUT VALIDATION
# ============================================================================
def main() -> None:
    """
    Main function to handle user input and run the expense splitting calculation.
    Includes comprehensive input validation and error handling to ensure
    a smooth user experience.
    """

    # MAIN INPUT VALIDATION LOOP
    # Continue until all inputs are valid and calculation is complete
    while True:
        try:
            # ================================================================
            # TOTAL AMOUNT INPUT AND VALIDATION
            # ================================================================

            # TOTAL AMOUNT COLLECTION
            # Get the total expense amount that needs to be split
            total_amount: float = float(input("Please enter the total amount of your expenses: "))

            # POSITIVE AMOUNT VALIDATION
            # Ensure amount is positive (negative expenses don't make logical sense)
            if total_amount <= 0:
                raise ValueError("Total amount must be positive.")

            # ================================================================
            # NUMBER OF PEOPLE INPUT AND VALIDATION
            # ================================================================

            # PEOPLE COUNT COLLECTION
            # Get number of people who will share the expenses
            number_of_people: int = int(input("Please enter the number of people: "))

            # MINIMUM PEOPLE VALIDATION
            # Ensure at least 1 person (though calculate_split will require 2+)
            if number_of_people <= 0:
                raise ValueError("Number of people must be positive.")

            # ================================================================
            # CALCULATION EXECUTION
            # ================================================================

            # EXPENSE SPLITTING CALCULATION
            # Call the main calculation function with validated inputs
            # This function handles its own validation for number_of_people > 1
            calculate_split(total_amount, number_of_people)

            # SUCCESSFUL COMPLETION
            # Break out of input loop after successful calculation
            break

        # ERROR HANDLING
        # Catch all ValueError exceptions (both conversion and validation errors)
        except ValueError as e:
            # USER-FRIENDLY ERROR FEEDBACK
            # Provide clear error message without technical details
            # Include specific error details when available
            print(f"Please enter a valid number. {str(e)}")
            # Loop continues, asking for input again


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    # Execute main function only when script is run directly
    # (not when imported as a module)
    # This is a Python best practice for executable scripts
    main()
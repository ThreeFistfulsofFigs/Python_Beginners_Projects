# ============================================================================
# BLACKJACK GAME
# ============================================================================
# This script implements a console-based Blackjack game where a user plays
# against a computer dealer. The game uses a standard deck with aces valued at
# 1 or 11, and face cards at 10. It includes logic for dealing cards, calculating
# scores, handling blackjacks, and determining the winner based on standard
# Blackjack rules. The console is cleared between games for a clean interface,
# and a logo is displayed using the 'art' library.
# ============================================================================

# Import required libraries
import random  # For selecting random cards from the deck
import os  # For clearing the console
from art import logo  # For displaying the game logo


# ============================================================================
# CONSOLE UTILITY FUNCTION
# ============================================================================

def clear_console():
    """
    Clear the console for a fresh game display.

    Uses platform-specific commands to clear the console, ensuring compatibility
    with Windows ('nt') and Unix-based systems.
    """
    # CONSOLE CLEARING
    # Execute 'cls' for Windows or 'clear' for Unix-based systems
    os.system('cls' if os.name == 'nt' else 'clear')


# ============================================================================
# CARD DEALING FUNCTION
# ============================================================================

def deal_card():
    """
    Select and return a random card from the deck.

    Returns:
        int: A card value from the deck (2-10 for numbered cards, 10 for face cards, 11 for aces).
    """
    # CARD SELECTION
    # Choose a random card from the global cards list
    return random.choice(cards)


# ============================================================================
# SCORE CALCULATION FUNCTION
# ============================================================================

def calculate_score(hand):
    """
    Calculate the total score of a hand, adjusting for aces.

    Args:
        hand (list): List of integers representing card values in the hand.

    Returns:
        int: The total score of the hand, with aces adjusted to avoid busting.
    """
    # INITIAL SCORE
    # Sum all card values in the hand
    score = sum(hand)
    num_aces = hand.count(11)

    # ACE ADJUSTMENT
    # Reduce score by 10 for each ace if over 21, converting ace from 11 to 1
    while score > 21 and num_aces > 0:
        score -= 10  # Subtract 10 to convert an ace from 11 to 1
        num_aces -= 1

    return score


# ============================================================================
# BLACKJACK CHECK FUNCTION
# ============================================================================

def is_blackjack(hand):
    """
    Check if a hand is a blackjack (Ace + 10-value card with exactly two cards).

    Args:
        hand (list): List of integers representing card values in the hand.

    Returns:
        bool: True if the hand is a blackjack, False otherwise.
    """
    # BLACKJACK VALIDATION
    # Check for two cards totaling 21
    return len(hand) == 2 and calculate_score(hand) == 21


# ============================================================================
# HAND DISPLAY FUNCTION
# ============================================================================

def display_hands(user_hand, computer_hand, reveal_all=False):
    """
    Display the user's and computer's hands and scores.

    Args:
        user_hand (list): List of integers representing the user's card values.
        computer_hand (list): List of integers representing the computer's card values.
        reveal_all (bool): If True, show the computer's full hand; otherwise, hide all but the first card.
    """
    # USER HAND DISPLAY
    # Show user's hand and calculated score
    user_score = calculate_score(user_hand)
    print(f"\nYour hand: {user_hand}, score: {user_score}")

    # COMPUTER HAND DISPLAY
    # Show full computer hand if reveal_all, otherwise show only the first card
    if reveal_all:
        computer_score = calculate_score(computer_hand)
        print(f"Computer's hand: {computer_hand}, score: {computer_score}")
    else:
        print(f"Computer's first card: [{computer_hand[0]}, ?]")


# ============================================================================
# MAIN GAME LOGIC
# ============================================================================

def play_blackjack():
    """
    Main function to orchestrate a game of Blackjack.

    Manages the game loop, including user input to start, dealing initial cards,
    handling player and computer turns, and determining the winner. Continues
    until the user chooses to exit.
    """
    # GAME LOOP
    # Continue until user chooses not to play
    while True:
        # START PROMPT
        # Ask user to start a new game
        play = input("Do you want to play a game of Blackjack? Type 'y' or 'n': ").lower()
        if play != 'y':
            print("Goodbye!")
            break

        # INITIAL SETUP
        # Clear console and display logo
        clear_console()
        print(logo)

        # DEAL CARDS
        # Give two cards each to user and computer
        user_hand = [deal_card(), deal_card()]
        computer_hand = [deal_card(), deal_card()]

        # BLACKJACK CHECK
        # Check for immediate blackjacks
        if is_blackjack(computer_hand):
            display_hands(user_hand, computer_hand, reveal_all=True)
            print("Computer has Blackjack! You lose!")
            continue
        elif is_blackjack(user_hand):
            display_hands(user_hand, computer_hand, reveal_all=True)
            print("You have Blackjack! You win!")
            continue

        # USER TURN
        # Allow user to hit or stand until they bust or choose to stand
        while True:
            display_hands(user_hand, computer_hand)
            user_score = calculate_score(user_hand)

            # BUST CHECK
            # End user's turn if score exceeds 21
            if user_score > 21:
                display_hands(user_hand, computer_hand, reveal_all=True)
                print("You went over 21! You lose!")
                break

            # HIT/STAND INPUT
            # Ask user to hit or stand
            hit = input("Type 'y' to get another card, 'n' to pass: ").lower()
            if hit != 'y':
                break
            # ADD CARD
            # Deal another card to user
            user_hand.append(deal_card())

        # USER BUST CHECK
        # Skip computer turn if user busted
        if calculate_score(user_hand) > 21:
            continue

        # COMPUTER TURN
        # Computer hits until score is at least 17
        computer_score = calculate_score(computer_hand)
        while computer_score <= 16:
            computer_hand.append(deal_card())
            computer_score = calculate_score(computer_hand)

        # WINNER DETERMINATION
        # Calculate final scores and determine winner
        user_score = calculate_score(user_hand)  # Recalculate to ensure accuracy
        display_hands(user_hand, computer_hand, reveal_all=True)

        # OUTCOME DISPLAY
        # Display result based on final scores
        if computer_score > 21:
            print("Computer went over 21. You win!")
        elif user_score > computer_score:
            print("You win!")
        elif computer_score > user_score:
            print("Computer wins!")
        else:
            print("It's a draw!")


# ============================================================================
# DECK DEFINITION
# ============================================================================

# DECK SETUP
# Define deck with ace as 11 and face cards as 10
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================

# GAME START
# Initiate the Blackjack game
play_blackjack()

# ============================================================================
# QUIZ LOGIC MANAGER
# ============================================================================
# This module defines the QuizBrain class, which manages the quiz game logic,
# including tracking the current question, checking answers, and maintaining
# the user's score. It processes a list of Question objects and handles user
# interaction via the console.
# ============================================================================

# ============================================================================
# QUIZ BRAIN CLASS DEFINITION
# ============================================================================

class QuizBrain:
    """
    A class to manage the quiz game logic and user interaction.

    Attributes:
        question_number (int): The current question number (starts at 0).
        question_list (list): List of Question objects for the quiz.
        n_correct (int): The number of correct answers provided by the user.
    """
    def __init__(self, q_list):
        """
        Initialize a new QuizBrain instance.

        Args:
            q_list (list): List of Question objects to be used in the quiz.
        """
        # ATTRIBUTE INITIALIZATION
        # Set up question tracking and score
        self.question_number = 0
        self.question_list = q_list
        self.n_correct = 0

    # ============================================================================
    # QUESTION STATUS CHECK
    # ============================================================================

    def still_has_question(self):
        """
        Check if there are remaining questions in the quiz.

        Returns:
            bool: True if there are more questions, False otherwise.
        """
        # QUESTION CHECK
        # Compare current question number to total questions
        return self.question_number < len(self.question_list)

    # ============================================================================
    # QUESTION PRESENTATION
    # ============================================================================

    def q_number(self):
        """
        Present the next question to the user and process their answer.
        """
        # QUESTION RETRIEVAL
        # Get the current question from the list
        current_q = self.question_list[self.question_number]

        # QUESTION COUNTER
        # Increment the question number
        self.question_number += 1

        # USER INPUT
        # Prompt user for their answer
        user_a = input(f"Question #{self.question_number}: {current_q.text} (True/False) ")

        # ANSWER VALIDATION
        # Check if the user's answer is correct
        self.check_answer(user_a, current_q.answer)

    # ============================================================================
    # ANSWER VALIDATION
    # ============================================================================

    def check_answer(self, user_a, correct_answer):
        """
        Check the user's answer against the correct answer and update score.

        Args:
            user_a (str): The user's answer (True or False).
            correct_answer (str): The correct answer to the question.
        """
        # ANSWER COMPARISON
        # Compare user's answer to the correct answer (case-insensitive)
        if user_a.lower() == correct_answer.lower():
            # CORRECT ANSWER
            # Increment score and display confirmation
            print("Correct Answer!")
            self.n_correct += 1
        else:
            # INCORRECT ANSWER
            # Display incorrect response
            print("Incorrect Answer!")

        # FEEDBACK DISPLAY
        # Show correct answer and current score
        print(f"The correct answer is: {correct_answer}")
        print(f"Your current score is {self.n_correct}/{self.question_number}. \n")
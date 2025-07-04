# ============================================================================
# QUESTION MODEL
# ============================================================================
# This module defines the Question class, which represents a single quiz question
# with its associated text and correct answer. It serves as a data structure for
# storing and accessing question details in the quiz game.
# ============================================================================

# ============================================================================
# QUESTION CLASS DEFINITION
# ============================================================================

class Question:
    """
    A class to represent a quiz question with its text and correct answer.

    Attributes:
        text (str): The text of the question.
        answer (str): The correct answer to the question (True or False).
    """
    def __init__(self, text, answer):
        """
        Initialize a new Question instance.

        Args:
            text (str): The text of the question.
            answer (str): The correct answer to the question (True or False).
        """
        # ATTRIBUTE ASSIGNMENT
        # Store the question text and answer
        self.text = text
        self.answer = answer
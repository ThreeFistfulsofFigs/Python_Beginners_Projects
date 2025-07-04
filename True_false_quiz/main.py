# ============================================================================
# QUIZ GAME MAIN PROGRAM
# ============================================================================
# This script implements a console-based quiz game that presents a series of
# true/false questions to the user. It utilizes the Question class to store
# questions, the QuizBrain class to manage the quiz logic, and a data module
# to provide the question dataset. The program tracks the user's score and
# displays the final results upon completion.
# ============================================================================

# IMPORTS
# Import required modules for question handling and quiz logic
from question_model import Question
from data import question_data
from quiz_brain import QuizBrain

# ============================================================================
# QUESTION BANK SETUP
# ============================================================================

# QUESTION INITIALIZATION
# Create a list to store Question objects
question_bank = []

# QUESTION POPULATION
# Iterate through question data to create Question objects and add to bank
for i in question_data:
    question = Question(i['question'], i['correct_answer'])
    question_bank.append(question)

# ============================================================================
# QUIZ EXECUTION
# ============================================================================

# QUIZ INITIALIZATION
# Create a QuizBrain instance with the question bank
quiz = QuizBrain(question_bank)

# SCORE TRACKING
# Initialize counter for correct answers
n_correct = 0

# QUIZ LOOP
# Continue presenting questions until none remain
while quiz.still_has_question():
    quiz.q_number()

# FINAL SCORE DISPLAY
# Show the user's final score and total questions
print(f"You have completed the quiz. Your final score is {quiz.n_correct}/{quiz.question_number}")
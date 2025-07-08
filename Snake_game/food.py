# ============================================================================
# FOOD MODULE
# ============================================================================
# This script defines the Food class for a Snake game, using the Turtle library
# to create and manage a food object that appears at random positions on the
# screen for the snake to consume.
# ============================================================================

# Import required libraries
from turtle import Turtle
import random  # For generating random positions

class Food(Turtle):
    def __init__(self):
        """
        Initialize the Food object.

        Sets up the food as a small blue circle, places it at a random position
        within the game boundaries, and configures its appearance and speed.
        """
        # INHERITANCE SETUP
        # Initialize Turtle parent class
        super().__init__()
        # FOOD CONFIGURATION
        # Set shape, size, and color
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.color("blue")
        self.speed("fastest")
        # INITIAL POSITION
        # Place food at random coordinates
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y)
        
    def refresh(self):
        """
        Move the food to a new random position.

        Generates new random coordinates within the game boundaries and moves
        the food to that position.
        """
        # POSITION UPDATE
        # Generate and set new random coordinates
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y)
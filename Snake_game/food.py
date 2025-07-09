# ============================================================================
# FOOD MODULE
# ============================================================================
# This module defines the Food class for a Snake game, utilizing the Turtle
# library to create and manage a food object that spawns at random positions
# on the game screen for the snake to consume.
# ============================================================================

# Import required libraries
from turtle import Turtle
import random  # For generating random coordinates

class Food(Turtle):
    def __init__(self):
        """
        Initialize the Food object.

        Configures the food as a small blue circle, sets its initial random
        position within the game boundaries, and adjusts its appearance and
        movement speed.
        """
        # INHERITANCE SETUP
        # Call Turtle parent class constructor
        super().__init__()
        # FOOD CONFIGURATION
        # Set shape, size, color, and speed
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.color("blue")
        self.speed("fastest")
        # INITIAL POSITION
        # Place food at a random position within boundaries
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y)
        
    def refresh(self):
        """
        Reposition the food to a new random location.

        Generates new random coordinates within the game boundaries and moves
        the food to that position.
        """
        # POSITION UPDATE
        # Assign new random coordinates
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y)
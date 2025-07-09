# ============================================================================
# PADDLE MODULE
# ============================================================================
# This module defines the Paddle class for a Pong game, utilizing the Turtle
# library to create and manage paddle objects that players can control to
# hit the ball. Each paddle can move up and down within the game boundaries.
# ============================================================================

# Import required libraries
from turtle import Turtle

class Paddle(Turtle):
    def __init__(self, position):
        """
        Initialize the Paddle object.

        Configures the paddle as a white rectangular shape, positions it at
        the specified location, and sets up its visual properties for gameplay.

        Args:
            position (tuple): The (x, y) coordinates for the paddle's starting position.
        """
        # INHERITANCE SETUP
        # Call Turtle parent class constructor
        super().__init__()
        # PADDLE CONFIGURATION
        # Set shape, color, size, and disable pen drawing
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        # INITIAL POSITION
        # Place paddle at specified starting position
        self.goto(position)

    def go_up(self):
        """
        Move the paddle upward by 25 units.

        Calculates new y-coordinate by adding 25 to current position and
        moves the paddle to the new location while maintaining x-coordinate.
        """
        # UPWARD MOVEMENT
        # Calculate new y-coordinate and move paddle up
        new_y = self.ycor() + 25
        self.goto(self.xcor(), new_y)
        
    def go_down(self):
        """
        Move the paddle downward by 25 units.

        Calculates new y-coordinate by subtracting 25 from current position and
        moves the paddle to the new location while maintaining x-coordinate.
        """
        # DOWNWARD MOVEMENT
        # Calculate new y-coordinate and move paddle down
        new_y = self.ycor() - 25
        self.goto(self.xcor(), new_y)

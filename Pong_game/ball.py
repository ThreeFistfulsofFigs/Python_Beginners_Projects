# ============================================================================
# BALL MODULE
# ============================================================================
# This module defines the Ball class for a Pong game, utilizing the Turtle
# library to create and manage a ball object that moves across the screen,
# bounces off walls and paddles, and resets when scoring occurs.
# ============================================================================

# Import required libraries
from turtle import Turtle

class Ball(Turtle):
    def __init__(self, position):
        """
        Initialize the Ball object.

        Configures the ball as a violet circle, sets its initial position,
        and establishes movement vectors for horizontal and vertical motion.

        Args:
            position (tuple): The (x, y) coordinates for the ball's starting position.
        """
        # INHERITANCE SETUP
        # Call Turtle parent class constructor
        super().__init__()
        # BALL CONFIGURATION
        # Set shape, color, and disable pen drawing
        self.shape("circle")
        self.color("violet")
        self.penup()
        # INITIAL POSITION
        # Place ball at specified starting position
        self.goto(position)
        # MOVEMENT VECTORS
        # Set initial movement speed for x and y directions
        self.x_movement = 10
        self.y_movement = 10
    
    def move(self):
        """
        Move the ball by updating its position based on current movement vectors.

        Calculates new coordinates by adding movement vectors to current position
        and moves the ball to the new location.
        """
        # POSITION CALCULATION
        # Calculate new coordinates based on movement vectors
        new_x = self.xcor() + self.x_movement
        new_y = self.ycor() + self.y_movement
        # POSITION UPDATE
        # Move ball to new calculated position
        self.goto(new_x, new_y)
    
    def bounce_y(self):
        """
        Reverse the ball's vertical movement direction.

        Multiplies the y_movement vector by -1 to make the ball bounce
        vertically when hitting top or bottom walls.
        """
        # VERTICAL BOUNCE
        # Reverse y-direction movement
        self.y_movement *= -1
        
    def bounce_x(self):
        """
        Reverse the ball's horizontal movement direction.

        Multiplies the x_movement vector by -1 to make the ball bounce
        horizontally when hitting paddles.
        """
        # HORIZONTAL BOUNCE
        # Reverse x-direction movement
        self.x_movement *= -1
        
    def reset_ball(self):
        """
        Reset the ball to center position and reverse horizontal direction.

        Moves the ball back to the center of the screen and reverses its
        horizontal movement direction for the next serve.
        """
        # POSITION RESET
        # Move ball back to center position
        self.goto(0, 0)
        # DIRECTION CHANGE
        # Reverse horizontal movement for next serve
        self.bounce_x()

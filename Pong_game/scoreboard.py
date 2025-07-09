# ============================================================================
# SCOREBOARD MODULE
# ============================================================================
# This module defines the Scoreboard class for a Pong game, utilizing the Turtle
# library to display and manage scores for both players. The scoreboard shows
# the current score for left and right players and updates dynamically when
# points are scored.
# ============================================================================

# Import required libraries
from turtle import Turtle   

class Scoreboard(Turtle):
    def __init__(self):
        """
        Initialize the Scoreboard object.

        Configures the scoreboard as a Turtle object, sets up visual properties,
        initializes both player scores to zero, and displays the initial scoreboard.
        The turtle is hidden to show only the score text.
        """
        # INHERITANCE SETUP
        # Call Turtle parent class constructor
        super().__init__()
        # SCOREBOARD CONFIGURATION
        # Set color, disable pen drawing, and hide turtle
        self.color("white")
        self.penup()
        self.hideturtle()
        # SCORE INITIALIZATION
        # Initialize both player scores to zero
        self.l_score = 0
        self.r_score = 0
        # INITIAL DISPLAY
        # Display initial scoreboard with zero scores
        self.update_scoreboard()
        
    def update_scoreboard(self):
        """
        Update the scoreboard display with current scores.

        Clears the previous display and redraws both player scores at their
        designated positions on the screen using large, bold font.
        """
        # DISPLAY RESET
        # Clear previous scoreboard display
        self.clear()
        # LEFT SCORE DISPLAY
        # Position and display left player's score
        self.goto(-100, 200)
        self.write(self.l_score, align="center", font=("Arial", 60, "bold"))
        # RIGHT SCORE DISPLAY
        # Position and display right player's score
        self.goto(100, 200)
        self.write(self.r_score, align="center", font=("Arial", 60, "bold"))

    def l_point(self):
        """
        Increment the left player's score and update the display.

        Increases the left player's score by 1 and refreshes the scoreboard
        to reflect the new score.
        """
        # SCORE INCREMENT
        # Add 1 to left player's score
        self.l_score += 1
        # DISPLAY UPDATE
        # Refresh scoreboard with updated score
        self.update_scoreboard()
        
    def r_point(self):
        """
        Increment the right player's score and update the display.

        Increases the right player's score by 1 and refreshes the scoreboard
        to reflect the new score.
        """
        # SCORE INCREMENT
        # Add 1 to right player's score
        self.r_score += 1
        # DISPLAY UPDATE
        # Refresh scoreboard with updated score
        self.update_scoreboard()

# ============================================================================
# SCOREBOARD MODULE
# ============================================================================
# This script defines the Scoreboard class for a Snake game, using the Turtle
# library to display the current score and game-over message. The scoreboard is
# positioned at the top of the screen and updates dynamically as the player scores.
# ============================================================================

# Import required libraries
from turtle import Turtle
# CONSTANT DEFINITION
# Define alignment and font settings for text display
ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")

class Scoreboard(Turtle):
    def __init__(self):
        """
        Initialize the Scoreboard object.

        Sets up the scoreboard as a Turtle object, positions it at the top of the
        screen, and displays the initial score. The turtle is hidden to show only
        the text.
        """
        # INHERITANCE SETUP
        # Initialize Turtle parent class
        super().__init__()
        # SCORE INITIALIZATION
        # Set starting score to 0
        self.score = 0
        # TURTLE CONFIGURATION
        # Set color, position, and hide the turtle
        self.color("white")
        self.penup()
        self.goto(0, 270)
        # SCORE DISPLAY
        # Write initial score to the screen
        self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)
        self.hideturtle()
        
    def increase_score(self):
        """
        Increment the score and update the display.

        Increases the score by 1, clears the previous display, and redraws the
        updated score.
        """
        # SCORE UPDATE
        # Increment score by 1
        self.score += 1
        # DISPLAY REFRESH
        # Clear and redraw the updated score
        self.clear()
        self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)
        
    def game_over(self):
        """
        Display the game-over message.

        Moves the scoreboard to the center of the screen and displays 'GAME OVER'.
        """
        # POSITION UPDATE
        # Move to center of screen
        self.goto(0, 0)
        # GAME OVER DISPLAY
        # Write game-over message
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)
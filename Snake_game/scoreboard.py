# ============================================================================
# SCOREBOARD MODULE
# ============================================================================
# This module defines the Scoreboard class for a Snake game, utilizing the Turtle
# library to display and manage the current score and high score. The scoreboard
# is positioned at the top of the game window and updates dynamically as the
# player earns points or resets the game.
# ============================================================================

# Import required libraries
from turtle import Turtle
# CONSTANT DEFINITION
# Define text alignment and font style for scoreboard display
ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")

class Scoreboard(Turtle):
    def __init__(self):
        """
        Initialize the Scoreboard object.

        Configures the scoreboard as a Turtle object, positions it at the top of
        the screen, initializes the score to zero, loads the high score from a
        file, and displays the initial score. The turtle is hidden to show only
        the text.
        """
        # INHERITANCE SETUP
        # Call Turtle parent class constructor
        super().__init__()
        # SCORE INITIALIZATION
        # Set initial score to 0 and load high score from file
        self.score = 0
        with open("data.txt", "r") as data:
            self.high_score = int(data.read())
            
        # TURTLE CONFIGURATION
        # Configure color, position, and hide the turtle
        self.color("white")
        self.penup()
        self.goto(0, 270)
        # SCORE DISPLAY
        # Display initial score and high score
        self.write(f"Score: {self.score}   High Score: {self.high_score}", align=ALIGNMENT, font=FONT)
        self.hideturtle()
        self.update()
        
    def increase_score(self):
        """
        Increment the score and refresh the display.

        Increases the score by 1 and updates the scoreboard display to reflect
        the new score while maintaining the high score.
        """
        # SCORE INCREMENT
        # Add 1 to the current score
        self.score += 1
        # DISPLAY UPDATE
        # Refresh the scoreboard with updated score
        self.update()
        
    def update(self):
        """
        Update the scoreboard display.

        Clears the previous scoreboard text and redraws the current score and
        high score at the designated position.
        """
        self.clear()
        self.write(f"Score: {self.score}     High Score: {self.high_score}", align=ALIGNMENT, font=FONT)
        
    def reset(self):
        """
        Reset the score and update the high score if necessary.

        Checks if the current score exceeds the high score, updates the high score
        if needed, saves it to a file, resets the current score to zero, and
        refreshes the display.
        """
        if self.score > self.high_score:
            self.high_score = self.score
            with open("data.txt", mode="w") as data:
                data.write(f"{self.high_score}")
                
        self.score = 0
        self.update()
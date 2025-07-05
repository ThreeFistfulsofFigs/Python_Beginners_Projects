# ============================================================================
# RANDOM TURTLE WALK
# ============================================================================
# This script uses Python's turtle module to create a visually engaging random
# walk pattern. A turtle moves in random directions (0, 90, 180, or 270 degrees)
# with random RGB colors for its pen, generating a unique geometric pattern on
# the screen. The program is designed for beginners to explore turtle graphics
# and randomization in Python, offering a simple yet creative visualization of
# random movement.
# ============================================================================

# Import required libraries
import random  # For generating random directions and colors
import turtle as t  # For turtle graphics functionality
from turtle import Screen  # For creating and managing the display window


# ============================================================================
# TURTLE SETUP
# ============================================================================

# TURTLE INITIALIZATION
# Create and configure the turtle object
to = t.Turtle()
to.speed(40)  # Set high speed for faster drawing
to.pensize(10)  # Set pen thickness for visibility
t.colormode(255)  # Enable 255-based RGB color mode for random colors
screen = Screen()  # Create screen object for user interaction


# ============================================================================
# COLOR GENERATION FUNCTION
# ============================================================================

def random_color() -> tuple[int, int, int]:
    """
    Generate a random RGB color tuple for the turtle's pen.

    Returns:
        tuple[int, int, int]: A tuple of three integers representing RGB values (0-255).

    Raises:
        None: The function uses random.randint, which is guaranteed to produce valid integers.
    """
    # COLOR GENERATION
    # Create random values for red, green, and blue components
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


# ============================================================================
# MAIN DRAWING LOGIC
# ============================================================================

# DIRECTION SETUP
# Define possible movement directions (in degrees)
directions = [0, 90, 180, 270]

# DRAWING LOOP
# Execute 500 steps of random movement with random colors
for _ in range(500):
    to.forward(50)  # Move turtle forward by 50 units
    to.setheading(random.choice(directions))  # Set random direction (0, 90, 180, or 270)
    to.pencolor(random_color())  # Set random pen color for the next segment

# SCREEN INTERACTION
# Keep window open until user clicks
screen.exitonclick()
# ============================================================================
# COLORFUL SPIROGRAPH
# ============================================================================
# This script uses Python's turtle graphics module to create a vibrant spirograph
# pattern by drawing a series of circles with random RGB colors and incremental
# rotations. The turtle draws 100 circles, each with a radius of 120 units,
# rotating 5 degrees after each circle, resulting in a layered, colorful design.
# The program exits when the user clicks the graphics window, making it ideal
# for beginners exploring turtle graphics and random color generation.
# ============================================================================

# Import required libraries
import turtle as t  # For creating graphical patterns
from turtle import Screen  # For managing the graphics window
import random  # For generating random RGB colors

# ============================================================================
# SCREEN SETUP
# ============================================================================
# Initialize the graphics window and configure color mode
screen = Screen()
screen.colormode(255)  # Set color mode to RGB (0-255) for random colors

# ============================================================================
# TURTLE CONFIGURATION
# ============================================================================
# Create and configure the turtle for drawing
to = t.Turtle()
to.speed("fastest")  # Set drawing speed to maximum for quick rendering
to.shape("circle")   # Set turtle shape to circle for visual appeal

# ============================================================================
# COLOR GENERATION FUNCTION
# ============================================================================
def random_color():
    """
    Generate a random RGB color tuple for the turtle's pen.

    Returns:
        tuple: A tuple of three integers (R, G, B) between 0 and 255.
    """
    # COLOR GENERATION
    # Create random values for red, green, and blue components
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

# ============================================================================
# DRAWING LOGIC
# ============================================================================
# Draw the spirograph pattern with random colors
for i in range(100):
    # COLOR APPLICATION
    # Set a new random color for the pen before drawing each circle
    to.pencolor(random_color())
    
    # CIRCLE DRAWING
    # Draw a circle with a fixed radius of 120 units
    to.circle(120)
    
    # ROTATION
    # Rotate the turtle 5 degrees to create the spirograph effect
    to.right(5)

# ============================================================================
# PROGRAM EXIT
# ============================================================================
# Close the graphics window when the user clicks
screen.exitonclick()
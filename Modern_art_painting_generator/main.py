# ============================================================================
# MODERN ART GENERATOR
# ============================================================================
# This script creates a modern art piece using the Turtle graphics module by
# drawing a grid of colored dots with random colors from a predefined list.
# The resulting artwork is saved as a PNG image.
# ============================================================================

# Import required libraries
import random  # For random color selection
import os  # For file operations
import turtle as turtle_module  # For drawing graphics
from PIL import ImageGrab  # For capturing and saving the canvas as an image


# ============================================================================
# COLOR EXTRACTION REFERENCE
# ============================================================================
# METHOD TO EXTRACT COLORS FROM PICTURE
# rgb_colors = []
# colors = colorgram.extract('image.jpg', 80)
# for color in colors:
#     r = color.rgb.r
#     g = color.rgb.g
#     b = color.rgb.b
#     new_color = (r, g, b)
#     rgb_colors.append(new_color)

# ============================================================================
# TURTLE GRAPHICS SETUP AND DRAWING
# ============================================================================
def main() -> None:
    """
    Main function to set up Turtle graphics, draw a grid of colored dots, and save
    the output as a PNG image.

    Returns:
        None: Draws the artwork and saves it as a PNG file
    """
    # TURTLE INITIALIZATION
    # Set up the Turtle object and screen
    to = turtle_module.Turtle()
    to.speed(40)
    turtle_module.colormode(255)
    screen = turtle_module.Screen()

    # TURTLE CONFIGURATION
    # Configure Turtle for drawing
    to.speed("fastest")
    to.penup()
    to.shape("blank")
    to.setheading(225)
    to.forward(300)
    to.setheading(0)
    number_of_dots = 100
    color_list = [(233, 233, 231), (230, 232, 236), (235, 231, 233), (227, 233, 229),
                  (206, 160, 84), (57, 88, 129), (143, 92, 43), (220, 205, 110),
                  (137, 27, 48), (134, 173, 199), (154, 48, 85), (45, 55, 104),
                  (131, 188, 144), (166, 159, 40), (82, 21, 44), (184, 93, 105),
                  (189, 140, 165), (42, 42, 62), (88, 120, 177), (57, 39, 33),
                  (88, 155, 93), (81, 153, 164), (194, 85, 71), (78, 73, 45),
                  (46, 74, 76), (162, 202, 218), (58, 126, 122), (219, 176, 187),
                  (171, 206, 171), (222, 180, 166), (179, 188, 212), (47, 74, 74),
                  (152, 35, 33), (45, 68, 67)]

    # DOT DRAWING LOOP
    # Draw a grid of dots with random colors
    for dot_count in range(1, number_of_dots + 1):
        # Draw a single dot with a random color
        to.dot(20, random.choice(color_list))
        to.forward(50)

        # Adjust position for new row after every 10 dots
        if dot_count % 10 == 0:
            to.setheading(90)
            to.forward(50)
            to.setheading(180)
            to.forward(500)
            to.setheading(0)

    # SAVE ARTWORK
    # Call function to save the drawing as a PNG
    save_as_png()

    # EXIT ON CLICK
    # Close the Turtle window when clicked
    screen.exitonclick()


# ============================================================================
# IMAGE SAVING FUNCTION
# ============================================================================
def save_as_png() -> None:
    """
    Saves the Turtle canvas as a PNG image by first saving as PostScript and
    then cropping and converting to PNG.

    Returns:
        None: Saves the image as 'modern_art_drawing.png' and removes temporary file
    """
    # CANVAS ACCESS
    # Get the Turtle canvas for saving
    canvas = turtle_module.getcanvas()

    # POSTSCRIPT SAVING
    # Save canvas as a temporary PostScript file
    canvas.postscript(file="temp.eps")

    # PNG CONVERSION
    # Capture the canvas area and save as PNG
    canvas.update()
    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()

    # SCREENSHOT AND SAVE
    # Crop the canvas area and save as PNG
    ImageGrab.grab().crop((x, y, x1, y1)).save("modern_art_drawing.png")

    # CLEANUP
    # Remove temporary PostScript file
    os.remove(os.path.abspath("temp.eps"))


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================
if __name__ == '__main__':
    # Execute main function only when script is run directly
    main()

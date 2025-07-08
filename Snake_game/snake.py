# ============================================================================
# SNAKE MODULE
# ============================================================================
# This script defines the Snake class for a Snake game, managing the creation,
# movement, and growth of the snake. The snake is composed of Turtle segments,
# moves in response to user input, and extends when food is consumed.
# ============================================================================

# Import required libraries
from turtle import Turtle 
# CONSTANT DEFINITION
# Define starting positions, movement distance, and direction angles
STARTING_POSITION = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
LEFT = 180
DOWN = 270
RIGHT = 0

class Snake:
    def __init__(self):
        """
        Initialize the Snake object.

        Creates an empty list for snake segments, builds the initial snake, and
        sets the head to the first segment.
        """
        # SEGMENT INITIALIZATION
        # Create empty list for segments
        self.segments = []
        # SNAKE CREATION
        # Build initial snake
        self.create_snake()
        # HEAD ASSIGNMENT
        # Set head to first segment
        self.head = self.segments[0]
        
    def create_snake(self):
        """
        Create the initial snake with three segments.

        Adds segments at predefined starting positions to form the initial snake.
        """
        # SEGMENT CREATION
        # Add segments at starting positions
        for position in STARTING_POSITION:
            self.add_segment(position)
            
    def add_segment(self, position):
        """
        Add a new segment to the snake at the specified position.

        Args:
            position (tuple): The (x, y) coordinates for the new segment.
        """
        # SEGMENT SETUP
        # Create and configure new square segment
        new_part = Turtle(shape="square")
        new_part.color("white")
        new_part.penup()
        new_part.goto(position)
        # SEGMENT ADDITION
        # Append segment to list
        self.segments.append(new_part)
        
    def extend_segment(self):
        """
        Extend the snake by adding a new segment at the tail.

        Adds a new segment at the position of the current tail segment.
        """
        # EXTENSION LOGIC
        # Add segment at tail's position
        self.add_segment(self.segments[-1].position())

    def move(self):
        """
        Move the snake forward one step.

        Updates the position of each segment to follow the one in front, then
        moves the head forward by the defined distance.
        """
        # SEGMENT MOVEMENT
        # Update each segment to the position of the one in front
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        # HEAD MOVEMENT
        # Move head forward
        self.head.forward(MOVE_DISTANCE)
        
    def up(self):
        """
        Turn the snake's head upward if not moving downward.

        Changes the head's direction to up (90 degrees) unless it is currently
        moving down, to prevent reversing.
        """
        # DIRECTION CHECK
        # Only turn if not moving down
        if self.head.heading() != DOWN:
            self.head.setheading(UP)
        
    def down(self):
        """
        Turn the snake's head downward if not moving upward.

        Changes the head's direction to down (270 degrees) unless it is currently
        moving up, to prevent reversing.
        """
        # DIRECTION CHECK
        # Only turn if not moving up
        if self.head.heading() != UP:
            self.head.setheading(DOWN)
    
    def left(self):
        """
        Turn the snake's head left if not moving right.

        Changes the head's direction to left (180 degrees) unless it is currently
        moving right, to prevent reversing.
        """
        # DIRECTION CHECK
        # Only turn if not moving right
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)
    
    def right(self):
        """
        Turn the snake's head right if not moving left.

        Changes the head's direction to right (0 degrees) unless it is currently
        moving left, to prevent reversing.
        """
        # DIRECTION CHECK
        # Only turn if not moving left
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)
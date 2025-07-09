# ============================================================================
# SNAKE MODULE
# ============================================================================
# This module defines the Snake class for a Snake game, managing the creation,
# movement, and growth of the snake. The snake is composed of Turtle segments
# that move in response to user input and extend upon consuming food.
# ============================================================================

# Import required libraries
from turtle import Turtle 
# CONSTANT DEFINITION
# Define starting positions, movement distance, and directional angles
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

        Creates an empty list for snake segments, constructs the initial snake
        with three segments, and designates the first segment as the head.
        """
        # SEGMENT INITIALIZATION
        # Initialize empty list for segments
        self.segments = []
        # SNAKE CREATION
        # Build initial snake with starting segments
        self.create_snake()
        # HEAD ASSIGNMENT
        # Set head to the first segment
        self.head = self.segments[0]
        
    def create_snake(self):
        """
        Create the initial snake with three segments.

        Adds segments at predefined starting positions to form the initial snake.
        """
        # SEGMENT CREATION
        # Add segments at starting coordinates
        for position in STARTING_POSITION:
            self.add_segment(position)
            
    def add_segment(self, position):
        """
        Add a new segment to the snake at the specified position.

        Args:
            position (tuple): The (x, y) coordinates for the new segment.
        """
        # SEGMENT SETUP
        # Create and configure a new square segment
        new_part = Turtle(shape="square")
        new_part.color("white")
        new_part.penup()
        new_part.goto(position)
        # SEGMENT ADDITION
        # Append segment to the segments list
        self.segments.append(new_part)
        
    def extend_segment(self):
        """
        Extend the snake by adding a new segment at the tail.

        Adds a new segment at the current position of the last segment (tail).
        """
        # EXTENSION LOGIC
        # Add a segment at the tail's current position
        self.add_segment(self.segments[-1].position())

    def move(self):
        """
        Move the snake forward one step.

        Updates each segment's position to follow the segment in front of it,
        then moves the head forward by the defined movement distance.
        """
        # SEGMENT MOVEMENT
        # Update each segment to the position of the one ahead
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        # HEAD MOVEMENT
        # Move the head forward by the movement distance
        self.head.forward(MOVE_DISTANCE)
        
    def up(self):
        """
        Turn the snake's head upward if not moving downward.

        Sets the head's direction to up (90 degrees) unless the snake is moving
        downward, preventing a 180-degree reversal.
        """
        # DIRECTION CHECK
        # Allow turn only if not moving down
        if self.head.heading() != DOWN:
            self.head.setheading(UP)
        
    def down(self):
        """
        Turn the snake's head downward if not moving upward.

        Sets the head's direction to down (270 degrees) unless the snake is moving
        upward, preventing a 180-degree reversal.
        """
        # DIRECTION CHECK
        # Allow turn only if not moving up
        if self.head.heading() != UP:
            self.head.setheading(DOWN)
    
    def left(self):
        """
        Turn the snake's head left if not moving right.

        Sets the head's direction to left (180 degrees) unless the snake is moving
        right, preventing a 180-degree reversal.
        """
        # DIRECTION CHECK
        # Allow turn only if not moving right
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)
    
    def right(self):
        """
        Turn the snake's head right if not moving left.

        Sets the head's direction to right (0 degrees) unless the snake is moving
        left, preventing a 180-degree reversal.
        """
        # DIRECTION CHECK
        # Allow turn only if not moving left
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)
            
    def reset(self):
        """
        Reset the snake to its initial state.

        Moves all segments off-screen, clears the segments list, recreates the
        initial snake, and reassigns the head to the first segment.
        """
        for seg in self.segments:
            seg.goto(1000, 1000)
        self.segments.clear()
        self.create_snake()
        self.head = self.segments[0]
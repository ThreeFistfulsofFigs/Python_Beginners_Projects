# ============================================================================
# SNAKE GAME MAIN MODULE
# ============================================================================
# This script orchestrates the Snake game, integrating the Snake, Food, and
# Scoreboard classes. It sets up the game window, handles user input, updates the
# game state, and detects collisions with walls, food, or the snake's tail.
# ============================================================================

# Import required libraries
import time  # For controlling game speed
from turtle import Screen  # For game window and input handling
from snake import Snake  # For snake object and movement
from food import Food  # For food object and placement
from scoreboard import Scoreboard  # For score display and game-over message

# ============================================================================
# GAME SETUP
# ============================================================================

# SCREEN CONFIGURATION
# Set up the game window
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)

# OBJECT INITIALIZATION
# Create snake, food, and scoreboard objects
snake = Snake()
food = Food()
scoreboard = Scoreboard()

# INPUT BINDING
# Bind arrow keys to snake movement functions
screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

# ============================================================================
# MAIN GAME LOOP
# ============================================================================

# GAME CONTROL
# Initialize game state
game_is_on = True
while game_is_on:
    # SCREEN UPDATE
    # Refresh screen to show updates
    screen.update()
    # GAME SPEED
    # Pause to control frame rate
    time.sleep(0.1)
    # SNAKE MOVEMENT
    # Move snake forward
    snake.move()
        
    # FOOD COLLISION DETECTION
    # Check if snake's head is close to food
    if snake.head.distance(food) < 15:
        # FOOD REPOSITION
        # Move food to new random location
        food.refresh()
        # SNAKE EXTENSION
        # Add new segment to snake
        snake.extend_segment()
        # SCORE UPDATE
        # Increment and display score
        scoreboard.increase_score()

    # WALL COLLISION DETECTION
    # Check if snake's head hits the wall
    if snake.head.xcor() > 285 or snake.head.xcor() < -295 or snake.head.ycor() > 285 or snake.head.ycor() < -285:
        scoreboard.reset()
        snake.reset()
    
    # TAIL COLLISION DETECTION
    # Check if snake's head hits its own tail
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            scoreboard.reset()
            snake.reset()
    
# GAME EXIT
# Wait for click to close window
screen.exitonclick()

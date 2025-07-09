# ============================================================================
# PONG GAME MAIN MODULE
# ============================================================================
# This script orchestrates the Pong game, integrating the Paddle, Ball, and
# Scoreboard classes. It sets up the game window, handles user input, updates
# the game state, and detects collisions with walls, paddles, and scoring zones.
# ============================================================================

# Import required libraries
from turtle import Screen  # For game window and input handling
from paddle import Paddle  # For paddle objects and movement
from ball import Ball      # For ball object and movement
import time                # For controlling game speed
from scoreboard import Scoreboard  # For score display and tracking

# ============================================================================
# GAME SETUP
# ============================================================================

# SCREEN CONFIGURATION
# Set up the game window with appropriate dimensions and styling
screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Pong")
screen.tracer(0)

# OBJECT INITIALIZATION
# Create paddle, ball, and scoreboard objects
r_paddle = Paddle((350, 0))    # Right paddle positioned on right side
l_paddle = Paddle((-350, 0))   # Left paddle positioned on left side
ball = Ball((0, 0))            # Ball starting at center
scoreboard = Scoreboard()       # Scoreboard for tracking points

# INPUT BINDING
# Bind keys to paddle movement functions
screen.listen()
screen.onkey(r_paddle.go_up, "Up")      # Right paddle up with Up arrow
screen.onkey(r_paddle.go_down, "Down")  # Right paddle down with Down arrow
screen.onkey(l_paddle.go_up, "w")       # Left paddle up with W key
screen.onkey(l_paddle.go_down, "s")     # Left paddle down with S key

# ============================================================================
# MAIN GAME LOOP
# ============================================================================

# GAME CONTROL
# Initialize game state
game_is_on = True
while game_is_on:
    # GAME SPEED
    # Control frame rate for smooth gameplay
    time.sleep(0.06)
    # SCREEN UPDATE
    # Refresh screen to show updates
    screen.update()
    # BALL MOVEMENT
    # Move ball forward based on current vectors
    ball.move()
    
    # WALL COLLISION DETECTION
    # Check if ball hits top or bottom walls
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()
        
    # PADDLE COLLISION DETECTION
    # Check if ball hits right paddle or left paddle
    if ball.distance(r_paddle) < 50 and ball.xcor() > 325 or ball.distance(l_paddle) < 50 and ball.xcor() < -325:
        ball.bounce_x()
        
    # LEFT SCORING ZONE
    # Check if ball passes right boundary (left player scores)
    if ball.xcor() < -380:
        ball.reset_ball()
        scoreboard.r_point()
    
    # RIGHT SCORING ZONE
    # Check if ball passes left boundary (right player scores)
    if ball.xcor() > 380:
        ball.reset_ball()
        scoreboard.l_point()

# GAME EXIT
# Wait for click to close window
screen.exitonclick()

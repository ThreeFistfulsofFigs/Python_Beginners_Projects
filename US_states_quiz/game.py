# ==========================================================
# US States Quiz Game Logic
# Description: Implements the core game functionality for the US States Quiz
# ==========================================================
import turtle
import time
import pandas as pd

# ==========================================================
# Game Class
# Description: Manages the game state, UI, and logic
# ==========================================================
class Game:
    # ------------------------------------------------------
    # Initialization
    # Description: Sets up the game screen, loads data, and initializes game state
    # ------------------------------------------------------
    def __init__(self):
        # Set up the screen
        self.screen = turtle.Screen()
        self.screen.title("U.S. States Game Quiz")
        self.image = "blank_states_img.gif"
        self.screen.setup(width=900, height=1100)
        self.screen.addshape(self.image)
        turtle.shape(self.image)

        # Load states data
        self.states = pd.read_csv("50_states.csv")
        self.all_states = self.states.state.to_list()
        self.guessed_states = []

        # Initialize game state
        self.game_on = True
        self.total_time = 300  # 5 minutes in seconds
        self.start_time = time.time()

        # Set up timer turtle
        self.timer_turtle = turtle.Turtle()
        self.timer_turtle.hideturtle()
        self.timer_turtle.penup()
        self.timer_turtle.goto(0, 350)  # Position timer at top
        
        # Start continuous timer
        self.schedule_timer_update()

    # ------------------------------------------------------
    # Timer Management
    # Description: Handles the game timer updates
    # ------------------------------------------------------
    def schedule_timer_update(self):
        """Schedule timer update using turtle's built-in timer"""
        if self.game_on:
            self.update_timer()
            self.screen.ontimer(self.schedule_timer_update, 1000)  # Update every 1000ms (1 second)

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, self.total_time - elapsed_time)
        mins, secs = divmod(int(remaining_time), 60)
        self.timer_turtle.clear()
        self.timer_turtle.write(f"Time: {mins:02d}:{secs:02d}", align="center", font=("Arial", 16, "normal"))
        
        if remaining_time <= 1:
            self.game_on = False
            
        return remaining_time

    # ------------------------------------------------------
    # State Placement
    # Description: Places a correctly guessed state on the map
    # ------------------------------------------------------
    def place_state(self, answer):
        state_turtle = turtle.Turtle()
        state_turtle.hideturtle()
        state_turtle.penup()
        state_data = self.states[self.states.state == answer]
        state_turtle.goto(state_data.x.item(), state_data.y.item())
        state_turtle.write(answer)

    # ------------------------------------------------------
    # Main Game Loop
    # Description: Runs the game, handles user input, and manages game flow
    # ------------------------------------------------------
    def run_game(self):
        while self.game_on:
            answer = self.screen.textinput(title=f"{len(self.guessed_states)}/{len(self.all_states)} States Guessed",
                                           prompt="Please enter a state (or 'Exit' to quit): ")

            if answer is None:  # Handle window close
                self.game_on = False
                break
                
            answer = answer.title()

            if answer == "Exit":
                self.game_on = False
                break

            if answer in self.all_states and answer not in self.guessed_states:
                self.guessed_states.append(answer)
                self.place_state(answer)

            if len(self.guessed_states) == len(self.all_states):
                self.game_on = False
                self.timer_turtle.clear()
                self.timer_turtle.write("Congratulations! All states guessed!", align="center",
                                        font=("Arial", 16, "bold"))

        # ------------------------------------------------------
        # Game End Handling
        # Description: Processes unguessed states and displays final results
        # ------------------------------------------------------
        if len(self.guessed_states) < len(self.all_states):
            missing_states = [state for state in self.all_states if state not in self.guessed_states]
            with open("missed_states.txt", "w") as f:
                for state in missing_states:
                    f.write(f"{state}\n")
            self.timer_turtle.clear()
            self.timer_turtle.write(f"Game Over! {len(self.guessed_states)}/{len(self.all_states)} states guessed.",
                                    align="center", font=("Arial", 16, "normal"))

        self.screen.exitonclick()
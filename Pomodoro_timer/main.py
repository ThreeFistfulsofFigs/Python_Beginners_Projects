# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Pomodoro Timer
# Description: A GUI-based Pomodoro Timer application using Tkinter.
#              Implements the Pomodoro Technique with customizable
#              work/break durations, multiple themes, progress ring,
#              motivational quotes, and session tracking with persistence.
# Author: [Your Name]
# Version: 1.0.0
# Dependencies: tkinter (standard library), winsound (Windows only)
# Last Modified: July 18, 2025
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import tkinter as tk
import math
import json
import os
from datetime import datetime, date
import random
import platform

# Conditional import for sound based on platform
if platform.system() == "Windows":
    import winsound
import threading

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
DARK_GREEN = "#4a7c59"
ORANGE = "#ff8c00"
PURPLE = "#8e44ad"
BLUE = "#3498db"

# Dark theme colors
DARK_BG = "#2c3e50"
DARK_FG = "#ecf0f1"
DARK_ACCENT = "#34495e"

FONT_NAME = "Courier"
DEFAULT_WORK_MIN = 25
DEFAULT_SHORT_BREAK_MIN = 5
DEFAULT_LONG_BREAK_MIN = 30

# ---------------------------- GLOBAL VARIABLES ------------------------------- #
reps = 0
timer = None
is_running = False
is_paused = False
total_time = 0
current_time = 0
is_dark_mode = False
current_theme = "default"
session_count_today = 0
total_focused_time_today = 0
session_history = []

# Customizable timer values
WORK_MIN = DEFAULT_WORK_MIN
SHORT_BREAK_MIN = DEFAULT_SHORT_BREAK_MIN
LONG_BREAK_MIN = DEFAULT_LONG_BREAK_MIN

# Motivational quotes
MOTIVATIONAL_QUOTES = [
    "Focus is the key to success!",
    "Every expert was once a beginner.",
    "Progress, not perfection.",
    "One pomodoro at a time.",
    "You're doing great!",
    "Stay focused, stay strong!",
    "Small steps lead to big changes.",
    "Consistency beats perfection.",
    "Your future self will thank you.",
    "Focus on the process, not just the outcome."
]

# Theme configurations
THEMES = {
    "default": {
        "bg": YELLOW,
        "fg": DARK_GREEN,
        "accent": GREEN,
        "timer_bg": YELLOW,
        "work_color": GREEN,
        "break_color": PINK,
        "long_break_color": RED
    },
    "dark": {
        "bg": DARK_BG,
        "fg": DARK_FG,
        "accent": BLUE,
        "timer_bg": DARK_BG,
        "work_color": BLUE,
        "break_color": PURPLE,
        "long_break_color": RED
    },
    "forest": {
        "bg": "#2d5016",
        "fg": "#90EE90",
        "accent": "#228B22",
        "timer_bg": "#2d5016",
        "work_color": "#32CD32",
        "break_color": "#98FB98",
        "long_break_color": "#FFD700"
    },
    "ocean": {
        "bg": "#001f3f",
        "fg": "#7FDBFF",
        "accent": "#0074D9",
        "timer_bg": "#001f3f",
        "work_color": "#39CCCC",
        "break_color": "#B10DC9",
        "long_break_color": "#FF4136"
    }
}

# ---------------------------- DATA PERSISTENCE ------------------------------- #
def load_settings():
    """Load settings from JSON file"""
    global WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN, current_theme, session_count_today, total_focused_time_today, session_history
    try:
        if os.path.exists("pomodoro_settings.json"):
            with open("pomodoro_settings.json", "r") as f:
                settings = json.load(f)
                WORK_MIN = settings.get("work_min", DEFAULT_WORK_MIN)
                SHORT_BREAK_MIN = settings.get("short_break_min", DEFAULT_SHORT_BREAK_MIN)
                LONG_BREAK_MIN = settings.get("long_break_min", DEFAULT_LONG_BREAK_MIN)
                # Validate theme
                loaded_theme = settings.get("theme", "default")
                current_theme = loaded_theme if loaded_theme in THEMES else "default"

                # Load today's stats
                today_str = str(date.today())
                if settings.get("last_date") == today_str:
                    session_count_today = settings.get("session_count_today", 0)
                    total_focused_time_today = settings.get("total_focused_time_today", 0)
                    session_history = settings.get("session_history", [])
                else:
                    # New day, reset stats
                    session_count_today = 0
                    total_focused_time_today = 0
                    session_history = []
    except Exception as e:
        print(f"Error loading settings: {e}")
        current_theme = "default"  # Fallback to default theme on error

def save_settings():
    """Save settings to JSON file"""
    settings = {
        "work_min": WORK_MIN,
        "short_break_min": SHORT_BREAK_MIN,
        "long_break_min": LONG_BREAK_MIN,
        "theme": current_theme,
        "last_date": str(date.today()),
        "session_count_today": session_count_today,
        "total_focused_time_today": total_focused_time_today,
        "session_history": session_history
    }
    try:
        with open("pomodoro_settings.json", "w") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print(f"Error saving settings: {e}")

# ---------------------------- SOUND FUNCTIONS ------------------------------- #
def play_notification_sound(sound_type):
    """Play notification sound based on session type"""

    def play_sound():
        try:
            if platform.system() == "Windows":
                if sound_type == "work_end":
                    winsound.Beep(800, 500)
                elif sound_type == "break_end":
                    winsound.Beep(600, 500)
                else:
                    winsound.Beep(700, 300)
            else:
                print("\a")  # System bell for non-Windows
        except:
            print("\a")  # Fallback

    sound_thread = threading.Thread(target=play_sound)
    sound_thread.daemon = True
    sound_thread.start()

# ---------------------------- THEME FUNCTIONS ------------------------------- #
def apply_theme(theme_name):
    """Apply selected theme to all widgets"""
    global current_theme
    current_theme = theme_name
    theme = THEMES[theme_name]

    # Update window and main widgets
    window.config(bg=theme["bg"])
    canvas.config(bg=theme["timer_bg"])
    timer_label.config(bg=theme["bg"], fg=theme["accent"])
    check_marks.config(bg=theme["bg"], fg=theme["accent"])
    stats_frame.config(bg=theme["bg"])
    stats_label.config(bg=theme["bg"], fg=theme["fg"])
    motivational_label.config(bg=theme["bg"], fg=theme["accent"])
    button_frame.config(bg=theme["bg"])  # Update button_frame background

    # Update buttons
    start_button.config(bg=theme["accent"], activebackground=theme["accent"])
    reset_button.config(bg=RED, activebackground="#ea5a7a")
    settings_button.config(bg=PURPLE, activebackground=PURPLE)
    theme_button.config(bg=BLUE, activebackground=BLUE)

    # Update help_label if it exists
    if 'help_label' in globals():
        help_label.config(bg=theme["bg"], fg="gray")

    save_settings()

def toggle_theme():
    """Cycle through all available themes"""
    theme_names = list(THEMES.keys())
    current_index = theme_names.index(current_theme)
    next_index = (current_index + 1) % len(theme_names)
    next_theme = theme_names[next_index]
    apply_theme(next_theme)

# ---------------------------- VISUAL FUNCTIONS ------------------------------- #
def update_progress_ring():
    """Update the progress ring around tomato and manage tomato visibility"""
    if total_time > 0:
        progress = (total_time - current_time) / total_time
        theme = THEMES[current_theme]

        center_x, center_y = 100, 112
        radius = 80

        canvas.delete("progress_ring")

        if is_running or current_time < total_time:
            canvas.itemconfig("tomato", state="hidden")
        else:
            canvas.itemconfig("tomato", state="normal")

        canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            outline="#ddd", width=6, fill="",
            tags="progress_ring"
        )

        if progress > 0:
            angle = 360 * progress
            if reps % 2 == 1:
                ring_color = RED if progress < 0.25 else ORANGE if progress < 0.75 else theme["work_color"]
            else:
                ring_color = theme["break_color"]

            pulse_width = 6
            if progress < 0.1 and is_running:
                pulse_width = 6 + int(2 * math.sin(current_time * 0.5))

            canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=90, extent=-angle,
                outline=ring_color, width=pulse_width, style="arc",
                tags="progress_ring"
            )
    else:
        canvas.itemconfig("tomato", state="normal")
        canvas.delete("progress_ring")

def get_timer_color():
    """Get timer text color based on urgency"""
    if total_time > 0:
        progress = (total_time - current_time) / total_time
        return "#ff6b6b" if progress < 0.25 else "#ffa726" if progress < 0.5 else "white"
    return "white"

def update_stats():
    """Update statistics display"""
    focused_hours = total_focused_time_today // 3600
    focused_minutes = (total_focused_time_today % 3600) // 60
    stats_text = f"Today: {session_count_today} sessions | {focused_hours}h {focused_minutes}m focused"
    stats_label.config(text=stats_text)

def update_checkmarks():
    """Update checkmarks display based on completed work sessions"""
    marks = ""
    completed_work_sessions = session_count_today % 4  # Only show up to 4 marks
    for i in range(4):
        if i < completed_work_sessions:
            marks += "✓"
        else:
            marks += "○"
    check_marks.config(text=marks)

def show_motivational_quote():
    """Display a random motivational quote"""
    quote = random.choice(MOTIVATIONAL_QUOTES)
    motivational_label.config(text=f"💡 {quote}")

# ---------------------------- SETTINGS WINDOW ------------------------------- #
def open_settings():
    """Open settings window"""
    settings_window = tk.Toplevel(window)
    settings_window.title("Settings")
    settings_window.config(bg=THEMES[current_theme]["bg"])
    settings_window.geometry("400x500")

    timer_frame = tk.LabelFrame(settings_window, text="Timer Settings",
                                bg=THEMES[current_theme]["bg"],
                                fg=THEMES[current_theme]["fg"])
    timer_frame.pack(padx=20, pady=10, fill="x")

    tk.Label(timer_frame, text="Work Duration (minutes):",
             bg=THEMES[current_theme]["bg"],
             fg=THEMES[current_theme]["fg"]).pack(anchor="w")
    work_var = tk.StringVar(value=str(WORK_MIN))
    work_entry = tk.Entry(timer_frame, textvariable=work_var, width=10)
    work_entry.pack(anchor="w", pady=5)

    tk.Label(timer_frame, text="Short Break Duration (minutes):",
             bg=THEMES[current_theme]["bg"],
             fg=THEMES[current_theme]["fg"]).pack(anchor="w")
    short_break_var = tk.StringVar(value=str(SHORT_BREAK_MIN))
    short_break_entry = tk.Entry(timer_frame, textvariable=short_break_var, width=10)
    short_break_entry.pack(anchor="w", pady=5)

    tk.Label(timer_frame, text="Long Break Duration (minutes):",
             bg=THEMES[current_theme]["bg"],
             fg=THEMES[current_theme]["fg"]).pack(anchor="w", pady=5)
    long_break_var = tk.StringVar(value=str(LONG_BREAK_MIN))
    long_break_entry = tk.Entry(timer_frame, textvariable=long_break_var, width=10)
    long_break_entry.pack(anchor="w", pady=5)

    theme_frame = tk.LabelFrame(settings_window, text="Theme Settings",
                                bg=THEMES[current_theme]["bg"],
                                fg=THEMES[current_theme]["fg"])
    theme_frame.pack(padx=20, pady=10, fill="x")

    theme_var = tk.StringVar(value=current_theme)
    for theme_name in THEMES.keys():
        tk.Radiobutton(theme_frame, text=theme_name.capitalize(),
                       variable=theme_var, value=theme_name,
                       bg=THEMES[current_theme]["bg"],
                       fg=THEMES[current_theme]["fg"],
                       selectcolor=THEMES[current_theme]["accent"]).pack(anchor="w")

    def apply_settings():
        global WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN
        try:
            WORK_MIN = int(work_var.get())
            SHORT_BREAK_MIN = int(short_break_var.get())
            LONG_BREAK_MIN = int(long_break_var.get())
            apply_theme(theme_var.get())
            save_settings()
            settings_window.destroy()
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid numbers for timer durations.")

    button_frame = tk.Frame(settings_window, bg=THEMES[current_theme]["bg"])
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Apply", command=apply_settings,
              bg=THEMES[current_theme]["accent"], fg="white").pack(side="left", padx=5)
    tk.Button(button_frame, text="Cancel", command=settings_window.destroy,
              bg=RED, fg="white").pack(side="left", padx=5)

# ---------------------------- TIMER FUNCTIONS ------------------------------- #
def reset_timer():
    """Reset timer to initial state"""
    global timer, is_running, is_paused, reps, total_time, current_time
    if timer:
        window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00", fill="white")
    timer_label.config(text="Timer", fg=THEMES[current_theme]["accent"])
    start_button.config(text="Start")
    is_running = False
    is_paused = False
    reps = 0
    total_time = 0
    current_time = 0
    canvas.itemconfig("tomato", state="normal")
    canvas.delete("progress_ring")
    update_checkmarks()  # Update checkmarks when resetting

def start_timer():
    """Start or resume timer, or pause if running"""
    global is_running, is_paused

    if not is_running and not is_paused:
        # Starting a new session
        start_new_session()
    elif is_running:
        # Pause the timer
        pause_timer()
    elif is_paused:
        # Resume the timer
        resume_timer()

def start_new_session():
    """Start a new timer session"""
    global reps, is_running, is_paused, total_time, current_time

    is_running = True
    is_paused = False
    start_button.config(text="Pause")
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    theme = THEMES[current_theme]

    if reps % 2 == 1:
        # Work session
        total_time = work_sec
        current_time = work_sec
        count_down(work_sec)
        timer_label.config(text="Work", fg=theme["work_color"])
    elif reps % 8 != 0:
        # Short break
        total_time = short_break_sec
        current_time = short_break_sec
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=theme["break_color"])
    else:
        # Long break
        total_time = long_break_sec
        current_time = long_break_sec
        count_down(long_break_sec)
        timer_label.config(text="Long Break", fg=theme["long_break_color"])

def pause_timer():
    """Pause the current timer"""
    global is_running, is_paused, timer

    is_running = False
    is_paused = True
    start_button.config(text="Resume")

    if timer:
        window.after_cancel(timer)

def resume_timer():
    """Resume the paused timer"""
    global is_running, is_paused

    is_running = True
    is_paused = False
    start_button.config(text="Pause")

    # Continue countdown from current_time
    count_down(current_time)

def count_down(count):
    """Count down timer"""
    global timer, is_running, reps, current_time, session_count_today, total_focused_time_today, session_history

    current_time = count
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    timer_color = get_timer_color()
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}", fill=timer_color)
    update_progress_ring()

    if count > 0 and is_running:
        timer = window.after(1000, count_down, count - 1)
    elif count == 0:
        # Timer finished
        session_completed()

def session_completed():
    """Handle session completion"""
    global is_running, is_paused, reps, session_count_today, total_focused_time_today, session_history

    is_running = False
    is_paused = False
    start_button.config(text="Start")

    if reps % 2 == 1:
        # Work session completed
        play_notification_sound("work_end")
        session_count_today += 1
        total_focused_time_today += WORK_MIN * 60
        session_history.append({
            "type": "work",
            "duration": WORK_MIN,
            "timestamp": datetime.now().isoformat()
        })
        update_stats()
        update_checkmarks()
        show_motivational_quote()
    else:
        # Break session completed
        play_notification_sound("break_end")

    # Reset for next session after long break cycle
    if reps % 8 == 0:
        reps = 0
        update_checkmarks()

    save_settings()
    # Auto-start next session
    start_timer()

# ---------------------------- KEYBOARD SHORTCUTS ------------------------------- #
def on_key_press(event):
    """Handle keyboard shortcuts"""
    if event.keysym == "space":
        start_timer()
    elif event.keysym == "r":
        reset_timer()
    elif event.keysym == "s":
        open_settings()
    elif event.keysym == "t":
        toggle_theme()

# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomodoro Timer")
window.config(padx=100, pady=50)

load_settings()

window.bind('<KeyPress>', on_key_press)
window.focus_set()

timer_label = tk.Label(text="Timer", font=(FONT_NAME, 40, "bold"), width=10)
timer_label.grid(row=0, column=1, padx=50, pady=50)

canvas = tk.Canvas(width=200, height=224, highlightthickness=0)
try:
    tomato_img = tk.PhotoImage(file="tomato.png")
    canvas.create_image(100, 112, image=tomato_img, tags="tomato")
except:
    canvas.create_oval(50, 50, 150, 150, fill=RED, outline=DARK_GREEN, width=3, tags="tomato")
    canvas.create_text(100, 100, text="🍅", font=(FONT_NAME, 40), tags="tomato")
timer_text = canvas.create_text(103, 112, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

check_marks = tk.Label(text="○○○○", font=(FONT_NAME, 20, "bold"))
check_marks.grid(row=3, column=1, pady=10)

stats_frame = tk.Frame()
stats_frame.grid(row=4, column=0, columnspan=3, pady=10)
stats_label = tk.Label(stats_frame, text="", font=(FONT_NAME, 10))
stats_label.pack()

motivational_label = tk.Label(text="Ready to focus? Let's go!", font=(FONT_NAME, 10, "italic"))
motivational_label.grid(row=5, column=0, columnspan=3, pady=5)

# Button frame and buttons
button_frame = tk.Frame(window, bg=THEMES[current_theme]["bg"])
button_frame.grid(row=2, column=1, pady=20)

# Start/Pause/Resume button
start_button = tk.Button(
    button_frame,
    text="Start",
    command=start_timer,
    width=8,
    fg="white",
    font=(FONT_NAME, 12, "bold"),
    relief="raised",
    bd=3
)
start_button.pack(side="left", padx=5)

# Reset button
reset_button = tk.Button(
    button_frame,
    text="Reset",
    command=reset_timer,
    width=8,
    bg=RED,
    fg="white",
    font=(FONT_NAME, 12, "bold"),
    relief="raised",
    bd=3,
    activebackground="#ea5a7a",
    activeforeground="white"
)
reset_button.pack(side="left", padx=5)

# Settings button
settings_button = tk.Button(
    button_frame,
    text="Settings",
    command=open_settings,
    width=8,
    bg=PURPLE,
    fg="white",
    font=(FONT_NAME, 12, "bold"),
    relief="raised",
    bd=3
)
settings_button.pack(side="left", padx=5)

# Theme toggle button
theme_button = tk.Button(
    button_frame,
    text="Theme",
    command=toggle_theme,
    width=8,
    bg=BLUE,
    fg="white",
    font=(FONT_NAME, 12, "bold"),
    relief="raised",
    bd=3
)
theme_button.pack(side="left", padx=5)

help_label = tk.Label(
    text="Shortcuts: Space=Start/Pause/Resume | R=Reset | S=Settings | T=Theme",
    font=(FONT_NAME, 8),
    fg="gray"
)
help_label.grid(row=6, column=0, columnspan=3, pady=10)

# Apply theme after all widgets are created
apply_theme(current_theme)
update_stats()
update_checkmarks()

def on_closing():
    save_settings()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()
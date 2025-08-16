# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Pomodoro Timer - Robust Version
# Description: A web-based Pomodoro Timer application using Streamlit.
#              Implements the Pomodoro Technique with customizable
#              work/break durations, multiple themes, progress bar,
#              motivational quotes, and session tracking with persistence.
#              ROBUST VERSION - Fixed all potential HTML/CSS issues.
# Version: 1.2.0 (Robust)
# Dependencies: streamlit, json, os, datetime, random, platform, time, math, base64
# Last Modified: August 16, 2025
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import streamlit as st
import json
import os
from datetime import datetime, date
import random
import platform
import time
import math
import base64

# Conditional import for sound based on platform
if platform.system() == "Windows":
    try:
        import winsound
    except ImportError:
        pass

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
DARK_GREEN = "#4a7c59"
ORANGE = "#ff8c00"
PURPLE = "#8e44ad"
BLUE = "#3498db"

# Theme colors
DARK_BG = "#2c3e50"
DARK_FG = "#ecf0f1"
DARK_ACCENT = "#34495e"

# Use web-safe fonts with fallbacks
FONT_NAME = "'Courier New', 'Lucida Console', 'Monaco', monospace"
DEFAULT_WORK_MIN = 25
DEFAULT_SHORT_BREAK_MIN = 5
DEFAULT_LONG_BREAK_MIN = 30

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
        "work_color": GREEN,
        "break_color": PINK,
        "long_break_color": RED
    },
    "dark": {
        "bg": DARK_BG,
        "fg": DARK_FG,
        "accent": BLUE,
        "work_color": BLUE,
        "break_color": PURPLE,
        "long_break_color": RED
    },
    "forest": {
        "bg": "#2d5016",
        "fg": "#90EE90",
        "accent": "#228B22",
        "work_color": "#32CD32",
        "break_color": "#98FB98",
        "long_break_color": "#FFD700"
    },
    "ocean": {
        "bg": "#001f3f",
        "fg": "#7FDBFF",
        "accent": "#0074D9",
        "work_color": "#39CCCC",
        "break_color": "#B10DC9",
        "long_break_color": "#FF4136"
    }
}


# ---------------------------- DATA PERSISTENCE ------------------------------- #
def load_settings():
    try:
        if os.path.exists("pomodoro_settings.json"):
            with open("pomodoro_settings.json", "r") as f:
                settings = json.load(f)
                st.session_state.WORK_MIN = settings.get("work_min", DEFAULT_WORK_MIN)
                st.session_state.SHORT_BREAK_MIN = settings.get("short_break_min", DEFAULT_SHORT_BREAK_MIN)
                st.session_state.LONG_BREAK_MIN = settings.get("long_break_min", DEFAULT_LONG_BREAK_MIN)
                loaded_theme = settings.get("theme", "default")
                st.session_state.current_theme = loaded_theme if loaded_theme in THEMES else "default"

                today_str = str(date.today())
                if settings.get("last_date") == today_str:
                    st.session_state.session_count_today = settings.get("session_count_today", 0)
                    st.session_state.total_focused_time_today = settings.get("total_focused_time_today", 0)
                    st.session_state.session_history = settings.get("session_history", [])
                else:
                    st.session_state.session_count_today = 0
                    st.session_state.total_focused_time_today = 0
                    st.session_state.session_history = []
    except Exception as e:
        st.error(f"Error loading settings: {e}")
        st.session_state.current_theme = "default"


def save_settings():
    settings = {
        "work_min": st.session_state.WORK_MIN,
        "short_break_min": st.session_state.SHORT_BREAK_MIN,
        "long_break_min": st.session_state.LONG_BREAK_MIN,
        "theme": st.session_state.current_theme,
        "last_date": str(date.today()),
        "session_count_today": st.session_state.session_count_today,
        "total_focused_time_today": st.session_state.total_focused_time_today,
        "session_history": st.session_state.session_history
    }
    try:
        with open("pomodoro_settings.json", "w") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        st.error(f"Error saving settings: {e}")


# ---------------------------- SOUND FUNCTIONS ------------------------------- #
def play_notification_sound(sound_type):
    try:
        # Fallback to simple beep
        print("\a")
    except:
        pass


# ---------------------------- THEME FUNCTIONS ------------------------------- #
def apply_theme(theme_name):
    st.session_state.current_theme = theme_name
    theme = THEMES[theme_name]

    # Escape any special characters in color values
    bg_color = str(theme['bg']).replace("'", "\\'").replace('"', '\\"')
    fg_color = str(theme['fg']).replace("'", "\\'").replace('"', '\\"')
    work_color = str(theme['work_color']).replace("'", "\\'").replace('"', '\\"')

    st.markdown(
        f"""
        <style>
            /* Multiple selectors for better compatibility */
            .stApp, [data-testid="stApp"], .main {{
                background-color: {bg_color} !important;
                color: {fg_color} !important;
            }}

            /* Simplified button styling - more robust */
            .stButton button {{
                color: white !important;
                border-radius: 8px !important;
                margin: 2px !important;
                font-weight: bold !important;
                min-height: 2.5rem !important;
                padding: 0.5rem 1rem !important;
            }}

            /* Removed fragile deep progress bar selector */
            /* Progress bar will use Streamlit's default styling */

            /* Safer heading styles */
            h1, h2, h3 {{
                text-align: center !important;
                color: {fg_color} !important;
            }}
            h1 {{
                font-size: clamp(2rem, 5vw, 3rem) !important;
                margin-bottom: 1rem !important;
            }}
            h2 {{
                font-size: clamp(1.5rem, 4vw, 2.25rem) !important;
                margin: 0.75rem 0 !important;
            }}
            h3 {{
                font-size: clamp(1.25rem, 3vw, 1.5rem) !important;
                margin: 0.5rem 0 !important;
            }}

            /* Responsive paragraph styling */
            p {{
                font-size: clamp(1rem, 2.5vw, 1.125rem) !important;
                margin: 0.5rem 0 !important;
                text-align: center !important;
            }}

            /* Custom classes - more reliable */
            .timer-display {{
                font-size: clamp(2rem, 6vw, 2.5rem) !important;
                font-weight: bold !important;
                font-family: {FONT_NAME} !important;
                color: {work_color} !important;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
                margin: 0.5rem 0 !important;
                text-align: center !important;
            }}

            .stats-text {{
                font-size: clamp(0.875rem, 2vw, 1rem) !important;
                color: {fg_color} !important;
                opacity: 0.8 !important;
                text-align: center !important;
            }}

            .checkmarks {{
                font-size: clamp(1.25rem, 3vw, 1.5rem) !important;
                letter-spacing: 0.5rem !important;
                color: {work_color} !important;
                text-align: center !important;
            }}

            /* Mobile-friendly responsive design */
            @media (max-width: 768px) {{
                .stButton button {{
                    min-width: 100% !important;
                    margin: 0.25rem 0 !important;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
    save_settings()


def toggle_theme():
    theme_names = list(THEMES.keys())
    current_index = theme_names.index(st.session_state.current_theme)
    next_index = (current_index + 1) % len(theme_names)
    next_theme = theme_names[next_index]
    apply_theme(next_theme)


# ---------------------------- VISUAL FUNCTIONS ------------------------------- #
def update_stats():
    focused_hours = st.session_state.total_focused_time_today // 3600
    focused_minutes = (st.session_state.total_focused_time_today % 3600) // 60
    return f"Today: {st.session_state.session_count_today} sessions | {focused_hours}h {focused_minutes}m focused"


def update_checkmarks():
    completed_work_sessions = st.session_state.session_count_today % 4
    marks = ""
    for i in range(4):
        marks += "✓" if i < completed_work_sessions else "○"
    return marks


def show_motivational_quote():
    quote = random.choice(MOTIVATIONAL_QUOTES)
    st.success(f"💡 {quote}")


def get_tomato_svg():
    """Create a simple, robust SVG tomato"""
    return """
    <div style="display: flex; justify-content: center; align-items: center; margin: 1.25rem 0;">
        <svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto;">
            <circle cx="100" cy="120" r="70" fill="#ff6b6b" stroke="#e55555" stroke-width="2"/>
            <ellipse cx="100" cy="70" rx="15" ry="8" fill="#4ecdc4"/>
            <ellipse cx="85" cy="65" rx="8" ry="12" fill="#45b7aa"/>
            <ellipse cx="115" cy="65" rx="8" ry="12" fill="#45b7aa"/>
            <path d="M85 65 Q100 50 115 65" stroke="#45b7aa" stroke-width="3" fill="none"/>
        </svg>
    </div>
    """


# ---------------------------- TIMER FUNCTIONS ------------------------------- #
def get_current_timer_seconds():
    """Calculate current remaining seconds based on timer state"""
    if not st.session_state.is_running and not st.session_state.is_paused:
        return st.session_state.total_time

    if st.session_state.is_paused and st.session_state.paused_at:
        elapsed = st.session_state.paused_at - st.session_state.start_time
    elif st.session_state.is_running and st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
    else:
        elapsed = 0

    remaining = max(0, st.session_state.total_time - elapsed)
    return remaining


def format_time(seconds):
    """Format seconds as MM:SS"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


def reset_timer():
    st.session_state.reps = 0
    st.session_state.is_running = False
    st.session_state.is_paused = False
    st.session_state.total_time = 0
    st.session_state.start_time = None
    st.session_state.paused_at = None
    st.session_state.timer_label = "Timer"
    st.session_state.session_completed = False
    save_settings()


def start_timer():
    if not st.session_state.is_running and not st.session_state.is_paused:
        st.session_state.reps += 1
        st.session_state.session_completed = False

        if st.session_state.reps % 2 == 1:
            # Work session
            st.session_state.total_time = st.session_state.WORK_MIN * 60
            st.session_state.timer_label = "Work"
        elif st.session_state.reps % 8 == 0:
            # Long break (every 4th break)
            st.session_state.total_time = st.session_state.LONG_BREAK_MIN * 60
            st.session_state.timer_label = "Long Break"
        else:
            # Short break
            st.session_state.total_time = st.session_state.SHORT_BREAK_MIN * 60
            st.session_state.timer_label = "Break"

    st.session_state.is_running = True
    st.session_state.is_paused = False
    st.session_state.start_time = time.time()
    st.session_state.paused_at = None
    save_settings()


def pause_timer():
    if st.session_state.is_running:
        st.session_state.is_running = False
        st.session_state.is_paused = True
        st.session_state.paused_at = time.time()
        save_settings()


def resume_timer():
    if st.session_state.is_paused:
        # Adjust start time to account for paused duration
        paused_duration = time.time() - st.session_state.paused_at
        st.session_state.start_time += paused_duration
        st.session_state.is_running = True
        st.session_state.is_paused = False
        st.session_state.paused_at = None
        save_settings()


def check_timer_completion():
    """Check if timer should complete and handle completion"""
    if st.session_state.is_running and not st.session_state.session_completed:
        remaining = get_current_timer_seconds()
        if remaining <= 0:
            complete_session()


def complete_session():
    """Handle session completion"""
    st.session_state.session_completed = True
    st.session_state.is_running = False
    st.session_state.is_paused = False
    st.session_state.paused_at = None

    # Track work sessions
    if st.session_state.reps % 2 == 1:  # Work session completed
        play_notification_sound("work_end")
        st.session_state.session_count_today += 1
        st.session_state.total_focused_time_today += st.session_state.WORK_MIN * 60
        st.session_state.session_history.append({
            "type": "work",
            "duration": st.session_state.WORK_MIN,
            "timestamp": datetime.now().isoformat()
        })
    else:  # Break session completed
        play_notification_sound("break_end")

    save_settings()


# ---------------------------- MAIN APP ------------------------------- #
def main():
    # Set page config for better mobile experience
    st.set_page_config(
        page_title="🍅 Pomodoro Timer",
        page_icon="🍅",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # Initialize session state
    if 'initialized' not in st.session_state:
        st.session_state.reps = 0
        st.session_state.is_running = False
        st.session_state.is_paused = False
        st.session_state.total_time = 0
        st.session_state.start_time = None
        st.session_state.paused_at = None
        st.session_state.current_theme = "forest"
        st.session_state.session_count_today = 0
        st.session_state.total_focused_time_today = 0
        st.session_state.session_history = []
        st.session_state.WORK_MIN = DEFAULT_WORK_MIN
        st.session_state.SHORT_BREAK_MIN = DEFAULT_SHORT_BREAK_MIN
        st.session_state.LONG_BREAK_MIN = DEFAULT_LONG_BREAK_MIN
        st.session_state.timer_label = "Timer"
        st.session_state.session_completed = False
        st.session_state.settings_expanded = False
        st.session_state.initialized = True
        load_settings()

    # Apply current theme
    apply_theme(st.session_state.current_theme)

    # Check for timer completion
    check_timer_completion()

    # Page title
    st.markdown("<h1>🍅 Pomodoro Timer</h1>", unsafe_allow_html=True)

    # Timer display with properly centered timer
    current_seconds = get_current_timer_seconds()
    time_display = format_time(current_seconds)

    # Create a container for the tomato and timer
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Display the SVG tomato
        st.markdown(get_tomato_svg(), unsafe_allow_html=True)

        # Display timer with robust centering
        st.markdown(f"""
        <div style="position: relative; text-align: center; margin-top: -6.875rem; margin-bottom: 5.625rem;">
            <span style="font-size: clamp(1.5rem, 4vw, 1.75rem); font-weight: bold; 
                         font-family: {FONT_NAME}; color: white; 
                         text-shadow: 2px 2px 4px rgba(0,0,0,0.9); display: inline-block;">
                {time_display}
            </span>
        </div>
        """, unsafe_allow_html=True)

    # Timer label
    st.markdown(f"<h2>{st.session_state.timer_label}</h2>", unsafe_allow_html=True)

    # Progress bar - using Streamlit's built-in styling
    if st.session_state.total_time > 0:
        progress = 1 - (current_seconds / st.session_state.total_time)
        progress = max(0, min(1, progress))  # Clamp between 0 and 1
    else:
        progress = 0

    # Use Streamlit's native progress bar
    st.progress(progress)

    # Session tracking
    st.markdown(f'<p class="checkmarks">{update_checkmarks()}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="stats-text">{update_stats()}</p>', unsafe_allow_html=True)

    # Show motivational quote when session completes
    if st.session_state.session_completed and st.session_state.reps % 2 == 1:
        show_motivational_quote()

    # Control buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if not st.session_state.is_running and not st.session_state.is_paused:
            button_text = "▶️ Start"
            if st.button(button_text, key="start", use_container_width=True):
                start_timer()
                st.rerun()
        elif st.session_state.is_running:
            button_text = "⏸️ Pause"
            if st.button(button_text, key="pause", use_container_width=True):
                pause_timer()
                st.rerun()
        else:  # is_paused
            button_text = "▶️ Resume"
            if st.button(button_text, key="resume", use_container_width=True):
                resume_timer()
                st.rerun()

    with col2:
        if st.button("🔄 Reset", key="reset", use_container_width=True):
            reset_timer()
            st.rerun()

    with col3:
        settings_text = "❌ Close" if st.session_state.settings_expanded else "⚙️ Settings"
        if st.button(settings_text, key="settings", use_container_width=True):
            st.session_state.settings_expanded = not st.session_state.settings_expanded
            st.rerun()

    with col4:
        theme_name = st.session_state.current_theme.title()
        if st.button(f"🎨 {theme_name}", key="theme", use_container_width=True):
            toggle_theme()
            st.rerun()

    # Settings panel
    if st.session_state.settings_expanded:
        st.markdown("---")
        st.markdown("<h3>⚙️ Settings</h3>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            work_min = st.number_input("Work Duration (minutes)",
                                       value=st.session_state.WORK_MIN,
                                       min_value=1, max_value=60, step=1)
            short_break_min = st.number_input("Short Break Duration (minutes)",
                                              value=st.session_state.SHORT_BREAK_MIN,
                                              min_value=1, max_value=30, step=1)
        with col2:
            long_break_min = st.number_input("Long Break Duration (minutes)",
                                             value=st.session_state.LONG_BREAK_MIN,
                                             min_value=1, max_value=60, step=1)
            theme_choice = st.selectbox("Theme",
                                        list(THEMES.keys()),
                                        index=list(THEMES.keys()).index(st.session_state.current_theme))

        if st.button("💾 Apply Settings", use_container_width=True):
            st.session_state.WORK_MIN = work_min
            st.session_state.SHORT_BREAK_MIN = short_break_min
            st.session_state.LONG_BREAK_MIN = long_break_min
            apply_theme(theme_choice)
            save_settings()
            st.session_state.settings_expanded = False
            st.success("Settings saved!")
            time.sleep(1)
            st.rerun()

    # Auto-refresh for timer updates
    if st.session_state.is_running:
        time.sleep(0.1)  # Small delay to prevent excessive CPU usage
        st.rerun()


if __name__ == "__main__":
    main()
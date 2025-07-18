# ==============================================================================
# Pomodoro Timer Application
# ==============================================================================
# Overview:
#   This is a Pomodoro timer application built using Kivy, designed to help users
#   manage work and break sessions effectively. It includes customizable timer
#   durations, theme switching (light/dark), session statistics, history tracking,
#   and motivational quotes.
#
# Purpose:
#   To provide a user-friendly interface for the Pomodoro Technique, enhancing
#   productivity with timed work sessions (25 minutes by default) and breaks
#   (5-minute short breaks, 30-minute long breaks after 4 sessions)
#
# Date:
#   Created: July 18, 2025
#   Last Modified: July 18, 2025
#
# Version:
#   1.0
#
# Key Features:
#   - Customizable work, short break, and long break durations
#   - Dark and light theme support with dynamic color updates
#   - Real-time session statistics (sessions, focused time, streak)
#   - Session history with scrollable log
#   - Motivational quotes for encouragement
#   - Keyboard shortcuts (Space: Start/Pause, R: Reset, S: Settings, T: Theme)
#   - Sound notifications for session transitions (Windows only)
#   - Persistent settings and history via JSON file
#
# Dependencies:
#   - Kivy (pip install kivy)
#   - winsound (Windows-specific for sound)
#
# Notes:
#   - Requires 'tomato.png' in the same directory for the timer image; a placeholder
#     is used if missing.
#   - Settings are saved to 'pomodoro_settings.json'.
#   - Theme colors are defined in the THEMES dictionary and applied dynamically.
# ==============================================================================

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import DictProperty, StringProperty
import math
import json
import os
from datetime import datetime, date
import random
import platform

# Conditional import for sound (Windows-specific)
if platform.system() == "Windows":
    import winsound
import threading

# ---------------------------- CONSTANTS ------------------------------- #
WARM_WHITE = (0.973, 0.945, 0.914, 1)  # #f8f1e9 (warm off-white background)
TOMATO_RED = (1.0, 0.251, 0.251, 1)  # #ff4040
CHECK_GREEN = (0.29, 0.439, 0.29, 1)  # #4a704a (muted green)
DARK_GRAY = (0.176, 0.176, 0.176, 1)  # #2d2d2d (darker text)
PINK = (0.886, 0.592, 0.612, 1)  # #e2979c (for breaks)
DARK_BG = (0.173, 0.243, 0.314, 1)  # #2c3e50 (dark theme)
WHITE = (1, 1, 1, 1)
LIGHT_GRAY = (0.5, 0.5, 0.5, 1)  # Added for better contrast in bright theme

# Font with emoji support (Windows path to Segoe UI Emoji with improved fallback)
if platform.system() == "Windows":
    EMOJI_FONT = "C:/Windows/Fonts/segoeuiemoji.ttf" if os.path.exists("C:/Windows/Fonts/segoeuiemoji.ttf") else \
        "C:/Windows/Fonts/seguiemj.ttf" if os.path.exists("C:/Windows/Fonts/seguiemj.ttf") else \
            "C:/Windows/Fonts/arialuni.ttf" if os.path.exists("C:/Windows/Fonts/arialuni.ttf") else "Roboto"
else:
    EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf" if os.path.exists(
        "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf") else "Roboto"
FONT_NAME = EMOJI_FONT  # Use emoji-capable font or fallback

DEFAULT_WORK_MIN = 25
DEFAULT_SHORT_BREAK_MIN = 5
DEFAULT_LONG_BREAK_MIN = 30

# ---------------------------- GLOBAL VARIABLES ------------------------------- #
reps = 0
timer_event = None
is_running = False
total_time = 0
current_time = 0
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
        "bg": WARM_WHITE,
        "fg": LIGHT_GRAY,  # Adjusted to LIGHT_GRAY for better label visibility
        "accent": TOMATO_RED,
        "timer_bg": WARM_WHITE,
        "work_color": CHECK_GREEN,
        "break_color": PINK,
        "long_break_color": TOMATO_RED,
        "button_bg": WARM_WHITE,
        "button_fg": DARK_GRAY
    },
    "dark": {
        "bg": DARK_BG,
        "fg": WHITE,
        "accent": (0.204, 0.596, 0.859, 1),
        "timer_bg": (0.1, 0.1, 0.1, 1),
        "work_color": (0.204, 0.596, 0.859, 1),
        "break_color": PINK,
        "long_break_color": TOMATO_RED,
        "button_bg": (0.3, 0.3, 0.3, 1),
        "button_fg": WHITE
    }
}


# ---------------------------- DATA PERSISTENCE ------------------------------- #
def load_settings():
    """Load settings from JSON file"""
    global WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN, session_count_today, total_focused_time_today, session_history
    try:
        if os.path.exists("pomodoro_settings.json"):
            with open("pomodoro_settings.json", "r") as f:
                settings = json.load(f)
                WORK_MIN = settings.get("work_min", DEFAULT_WORK_MIN)
                SHORT_BREAK_MIN = settings.get("short_break_min", DEFAULT_SHORT_BREAK_MIN)
                LONG_BREAK_MIN = settings.get("long_break_min", DEFAULT_LONG_BREAK_MIN)
                App.get_running_app().current_theme = settings.get("theme", "default")
                today_str = str(date.today())
                if settings.get("last_date") == today_str:
                    session_count_today = settings.get("session_count_today", 0)
                    total_focused_time_today = settings.get("total_focused_time_today", 0)
                    session_history = settings.get("session_history", [])
                else:
                    session_count_today = 0
                    total_focused_time_today = 0
                    session_history = []
    except Exception as e:
        print(f"Error loading settings: {e}")


def save_settings():
    """Save settings to JSON file"""
    settings = {
        "work_min": WORK_MIN,
        "short_break_min": SHORT_BREAK_MIN,
        "long_break_min": LONG_BREAK_MIN,
        "theme": App.get_running_app().current_theme,
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

    threading.Thread(target=play_sound, daemon=True).start()


# ---------------------------- CUSTOM WIDGETS ------------------------------- #
class StatsWidget(BoxLayout):
    """Widget to display session statistics"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 5
        self.size_hint_y = None
        self.height = 120

        # Title
        self.title_label = Label(text="📊 TODAY'S STATS", font_size=16, size_hint_y=None, height=30,
                                 color=DARK_GRAY, font_name=FONT_NAME, bold=True)  # Store reference
        self.add_widget(self.title_label)

        # Stats labels
        self.sessions_label = Label(text="Sessions: 0", font_size=14, size_hint_y=None, height=25,
                                    color=DARK_GRAY, font_name=FONT_NAME)
        self.time_label = Label(text="Focused Time: 0h 0m", font_size=14, size_hint_y=None, height=25,
                                color=DARK_GRAY, font_name=FONT_NAME)
        self.streak_label = Label(text="Current Streak: 0", font_size=14, size_hint_y=None, height=25,
                                  color=DARK_GRAY, font_name=FONT_NAME)

        self.add_widget(self.sessions_label)
        self.add_widget(self.time_label)
        self.add_widget(self.streak_label)

    def update_colors(self):
        """Update widget colors based on current theme"""
        app = App.get_running_app()
        text_color = WHITE if app.current_theme == "dark" else DARK_GRAY
        self.title_label.color = text_color  # Update title explicitly
        self.sessions_label.color = text_color
        self.time_label.color = text_color
        self.streak_label.color = text_color

    def update_stats(self, sessions, focused_time, streak=0):
        self.sessions_label.text = f"Sessions: {sessions}"
        hours = focused_time // 3600
        minutes = (focused_time % 3600) // 60
        self.time_label.text = f"Focused Time: {hours}h {minutes}m"
        self.streak_label.text = f"Current Streak: {streak}"


class HistoryWidget(BoxLayout):
    """Widget to display session history"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 5

        # Title
        self.title_label = Label(text="📈 SESSION HISTORY", font_size=16, size_hint_y=None, height=30,
                                 color=DARK_GRAY, font_name=FONT_NAME, bold=True)  # Store reference
        self.add_widget(self.title_label)

        # Scrollable history
        scroll = ScrollView(size_hint=(1, 1))
        self.history_layout = BoxLayout(orientation='vertical', spacing=2, size_hint_y=None)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        scroll.add_widget(self.history_layout)
        self.add_widget(scroll)

    def update_colors(self):
        """Update widget colors based on current theme"""
        app = App.get_running_app()
        text_color = WHITE if app.current_theme == "dark" else DARK_GRAY
        self.title_label.color = text_color  # Update title explicitly
        for child in self.history_layout.children:
            if isinstance(child, Label):
                child.color = text_color

    def add_session(self, session_type, duration, timestamp):
        app = App.get_running_app()
        time_str = datetime.fromisoformat(timestamp).strftime("%H:%M")
        emoji = "🍅" if session_type == "work" else "☕"
        session_text = f"{emoji} {time_str} - {session_type.title()} ({duration}min)"

        session_label = Label(text=session_text, font_size=12, size_hint_y=None, height=25,
                              color=DARK_GRAY, font_name=FONT_NAME, text_size=(None, None))
        self.history_layout.add_widget(session_label)


# ---------------------------- MAIN APP ------------------------------- #
class PomodoroApp(App):
    theme = DictProperty(THEMES["default"])
    font_name = StringProperty(FONT_NAME)  # Add font_name property
    current_theme = StringProperty("default")  # Add current_theme property

    def __init__(self):
        super().__init__()
        self.reps = 0
        self.timer_event = None
        self.is_running = False
        self.total_time = 0
        self.current_time = 0
        self.session_count_today = 0
        self.total_focused_time_today = 0
        self.session_history = []

    def build(self):
        load_settings()
        self.theme = THEMES[self.current_theme]
        Window.bind(on_keyboard=self.on_key_press)
        Window.clearcolor = self.theme["bg"]
        print("Loading KV string...")
        root = Builder.load_string(KV)
        print("KV string loaded successfully.")
        return root

    def on_start(self):
        """Initialize the app after building and update widget colors"""
        self.update_stats()
        self.update_history()
        self.show_motivational_quote()  # Set initial motivational quote
        if hasattr(self.root.ids, 'stats_widget'):
            self.root.ids.stats_widget.update_colors()
        if hasattr(self.root.ids, 'history_widget'):
            self.root.ids.history_widget.update_colors()
        Clock.schedule_once(self.delayed_init, 0.1)
        print("App started, checking tomato.png...")
        if not os.path.exists("tomato.png"):
            print("Warning: tomato.png not found, using placeholder.")
            self.root.ids.tomato_widget.clear_widgets()
            self.root.ids.tomato_widget.add_widget(Label(text="[Tomato Image Missing]"))

    def delayed_init(self, dt):
        """Initialize widgets that need the root to be ready"""
        pass

    def apply_theme(self, theme_name):
        """Apply selected theme"""
        self.current_theme = theme_name
        self.theme = THEMES[theme_name]
        Window.clearcolor = self.theme["bg"]
        if hasattr(self.root.ids, 'stats_widget'):
            self.root.ids.stats_widget.update_colors()
        if hasattr(self.root.ids, 'history_widget'):
            self.root.ids.history_widget.update_colors()
        save_settings()

    def toggle_theme(self):
        """Toggle between themes"""
        new_theme = "dark" if self.current_theme == "default" else "default"
        self.apply_theme(new_theme)

    def update_stats(self):
        """Update statistics display"""
        if hasattr(self.root.ids, 'stats_widget'):
            self.root.ids.stats_widget.update_stats(
                self.session_count_today,
                self.total_focused_time_today,
                self.session_count_today  # Simple streak calculation
            )

    def update_history(self):
        """Update session history display"""
        if hasattr(self.root.ids, 'history_widget'):
            self.root.ids.history_widget.history_layout.clear_widgets()
            for session in self.session_history[-10:]:  # Show last 10 sessions
                self.root.ids.history_widget.add_session(
                    session["type"],
                    session["duration"],
                    session["timestamp"]
                )

    def show_motivational_quote(self):
        """Display motivational quote"""
        quote = random.choice(MOTIVATIONAL_QUOTES)
        if hasattr(self.root.ids, 'motivational_label'):
            self.root.ids.motivational_label.text = f"💡 {quote}"

    def open_settings(self):
        """Open settings popup"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Work duration
        content.add_widget(Label(text="Work Duration (minutes):", color=self.theme["fg"],
                                 font_name=FONT_NAME, font_size=14, size_hint_y=None, height=30))
        work_input = TextInput(text=str(WORK_MIN), multiline=False, font_name=FONT_NAME,
                               size_hint_y=None, height=40, background_color=self.theme["button_bg"],
                               foreground_color=DARK_GRAY if self.current_theme == "default" else WHITE)
        content.add_widget(work_input)

        # Short break duration
        content.add_widget(Label(text="Short Break Duration (minutes):", color=self.theme["fg"],
                                 font_name=FONT_NAME, font_size=14, size_hint_y=None, height=30))
        short_break_input = TextInput(text=str(SHORT_BREAK_MIN), multiline=False, font_name=FONT_NAME,
                                      size_hint_y=None, height=40, background_color=self.theme["button_bg"],
                                      foreground_color=DARK_GRAY if self.current_theme == "default" else WHITE)
        content.add_widget(short_break_input)

        # Long break duration
        content.add_widget(Label(text="Long Break Duration (minutes):", color=self.theme["fg"],
                                 font_name=FONT_NAME, font_size=14, size_hint_y=None, height=30))
        long_break_input = TextInput(text=str(LONG_BREAK_MIN), multiline=False, font_name=FONT_NAME,
                                     size_hint_y=None, height=40, background_color=self.theme["button_bg"],
                                     foreground_color=DARK_GRAY if self.current_theme == "default" else WHITE)
        content.add_widget(long_break_input)

        # Buttons
        button_layout = BoxLayout(spacing=10, size_hint_y=None, height=50)
        apply_button = Button(text="Apply", background_color=self.theme["accent"],
                              font_name=FONT_NAME, font_size=16, color=WHITE)
        cancel_button = Button(text="Cancel", background_color=TOMATO_RED,
                               font_name=FONT_NAME, font_size=16, color=WHITE)
        button_layout.add_widget(apply_button)
        button_layout.add_widget(cancel_button)
        content.add_widget(button_layout)

        popup = Popup(title="⚙️ Settings", content=content, size_hint=(0.8, 0.8),
                      title_color=WHITE if self.current_theme == "dark" else self.theme["fg"],
                      background_color=self.theme["bg"])

        def apply_settings(instance):
            global WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN
            try:
                WORK_MIN = int(work_input.text)
                SHORT_BREAK_MIN = int(short_break_input.text)
                LONG_BREAK_MIN = int(long_break_input.text)
                save_settings()
                popup.dismiss()
            except ValueError:
                popup.title = "❌ Error: Please enter valid numbers"

        apply_button.bind(on_press=apply_settings)
        cancel_button.bind(on_press=popup.dismiss)
        popup.open()

    def reset_timer(self):
        """Reset the timer"""
        global reps, timer_event, is_running, total_time, current_time
        if timer_event:
            Clock.unschedule(timer_event)
            timer_event = None
        self.reps = 0
        is_running = False
        total_time = 0
        current_time = 0
        self.root.ids.timer_label.text = "25:00"
        self.root.ids.timer_label.color = self.theme["fg"]
        self.root.ids.title_label.text = "🍅 POMODORO TIMER"
        self.root.ids.title_label.color = self.theme["accent"]
        self.root.ids.start_button.text = "START"
        self.root.ids.check_marks.text = "○ ○ ○ ○"
        self.show_motivational_quote()  # Reset to a new quote
        self.root.ids.motivational_label.text = "Ready to focus? Let's go! 🚀"

    def start_timer(self):
        """Start or pause the timer"""
        global reps, is_running, total_time, current_time
        if not is_running:
            is_running = True
            self.reps += 1

            if self.reps % 2 == 1:  # Work session
                total_time = WORK_MIN * 60
                current_time = total_time
                self.root.ids.title_label.text = "🍅 WORK SESSION"
                self.root.ids.title_label.color = self.theme["work_color"]
            elif self.reps % 8 != 0:  # Short break
                total_time = SHORT_BREAK_MIN * 60
                current_time = total_time
                self.root.ids.title_label.text = "☕ SHORT BREAK"
                self.root.ids.title_label.color = self.theme["break_color"]
            else:  # Long break
                total_time = LONG_BREAK_MIN * 60
                current_time = total_time
                self.root.ids.title_label.text = "🏖️ LONG BREAK"
                self.root.ids.title_label.color = self.theme["long_break_color"]

            self.root.ids.start_button.text = "PAUSE"
            self.timer_event = Clock.schedule_interval(self.count_down, 1)
        else:
            is_running = False
            self.root.ids.start_button.text = "START"
            if self.timer_event:
                Clock.unschedule(self.timer_event)

    def count_down(self, dt):
        """Update timer countdown"""
        global reps, is_running, current_time, total_time, session_count_today, total_focused_time_today, session_history

        if total_time <= 0:
            return

        current_time -= 1
        count_min = math.floor(current_time / 60)
        count_sec = current_time % 60

        # Update timer display
        self.root.ids.timer_label.text = f"{count_min:02d}:{count_sec:02d}"

        # Change color based on time remaining
        time_ratio = current_time / total_time
        if time_ratio < 0.25:
            self.root.ids.timer_label.color = TOMATO_RED
        elif time_ratio < 0.5:
            self.root.ids.timer_label.color = (1, 1, 0, 1)  # YELLOW
        else:
            self.root.ids.timer_label.color = self.theme["fg"]

        # Timer finished
        if current_time <= 0:
            is_running = False
            self.root.ids.start_button.text = "START"

            if self.reps % 2 == 1:  # Work session completed
                play_notification_sound("work_end")
                session_count_today += 1
                total_focused_time_today += WORK_MIN * 60
                session_history.append({
                    "type": "work",
                    "duration": WORK_MIN,
                    "timestamp": datetime.now().isoformat()
                })
                self.update_stats()
                self.update_history()
                self.show_motivational_quote()
            else:  # Break completed
                play_notification_sound("break_end")
                session_history.append({
                    "type": "break",
                    "duration": SHORT_BREAK_MIN if self.reps % 8 != 0 else LONG_BREAK_MIN,
                    "timestamp": datetime.now().isoformat()
                })
                self.update_history()

            # Update check marks
            if self.reps % 2 == 1:
                work_sessions = math.ceil(self.reps / 2)
                marks = "✓ " * work_sessions + "○ " * (4 - work_sessions)
                self.root.ids.check_marks.text = marks.strip()

            # Reset after 4 work sessions
            if self.reps % 8 == 0:
                self.reps = 0
                self.root.ids.check_marks.text = "○ ○ ○ ○"

            save_settings()
            # Auto-start next session
            Clock.schedule_once(lambda dt: self.start_timer(), 1)

    def on_key_press(self, window, key, scancode, codepoint, modifier):
        """Handle keyboard shortcuts"""
        if codepoint == ord(' '):
            self.start_timer()
        elif codepoint == ord('r'):
            self.reset_timer()
        elif codepoint == ord('s'):
            self.open_settings()
        elif codepoint == ord('t'):
            self.toggle_theme()
        return True


# ---------------------------- KIVY UI LAYOUT ------------------------------- #
KV = '''
#:import StatsWidget __main__.StatsWidget
#:import HistoryWidget __main__.HistoryWidget

BoxLayout:
    orientation: 'horizontal'
    padding: 20
    spacing: 20

    # Left panel - Timer
    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.6
        spacing: 20

        # Title
        Label:
            id: title_label
            text: '🍅 POMODORO TIMER'
            font_name: app.font_name
            font_size: 32
            size_hint_y: None
            height: 60
            color: app.theme['accent']
            bold: True

        # Tomato widget
        RelativeLayout:
            id: tomato_widget
            size_hint_y: None
            height: 250
            Image:
                source: 'tomato.png'
                size_hint: None, None
                size: self.parent.height * 0.7, self.parent.height * 0.7
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}

        # Timer display
        Label:
            id: timer_label
            text: '25:00'
            font_name: app.font_name
            font_size: 48
            color: app.theme['fg']
            size_hint_y: None
            height: 80
            bold: True

        # Control buttons
        BoxLayout:
            size_hint_y: None
            height: 60
            spacing: 15

            Button:
                id: start_button
                text: 'START'
                font_name: app.font_name
                font_size: 18
                background_color: app.theme['accent']
                color: 1, 1, 1, 1
                bold: True
                on_press: app.start_timer()

            Button:
                id: reset_button
                text: 'RESET'
                font_name: app.font_name
                font_size: 18
                background_color: app.theme['button_bg']
                color: app.theme['button_fg']
                bold: True
                on_press: app.reset_timer()

            Button:
                id: settings_button
                text: 'SETTINGS'
                font_name: app.font_name
                font_size: 18
                background_color: app.theme['button_bg']
                color: app.theme['button_fg']
                bold: True
                on_press: app.open_settings()

            Button:
                id: theme_button
                text: 'THEME'
                font_name: app.font_name
                font_size: 18
                background_color: app.theme['button_bg']
                color: app.theme['button_fg']
                bold: True
                on_press: app.toggle_theme()

        # Progress indicators
        Label:
            id: check_marks
            text: '○ ○ ○ ○'
            font_name: app.font_name
            font_size: 24
            size_hint_y: None
            height: 40
            color: app.theme['accent']

        # Motivational message
        Label:
            id: motivational_label
            font_name: app.font_name
            font_size: 14
            size_hint_y: None
            height: 30
            color: app.theme['accent']
            italic: True

        # Help text
        Label:
            id: help_label
            text: 'Shortcuts: Space=Start/Pause | R=Reset | S=Settings | T=Theme'
            font_name: app.font_name
            font_size: 10
            height: 20
            color: app.theme['fg']
            opacity: 0.7

    # Right panel - Stats and History
    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.4
        spacing: 20

        # Stats widget
        StatsWidget:
            id: stats_widget

        # History widget
        HistoryWidget:
            id: history_widget
'''

if __name__ == '__main__':
    PomodoroApp().run()

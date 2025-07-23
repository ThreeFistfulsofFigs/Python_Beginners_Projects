# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                          Flashcard Language Learning App                   ║
# ║  GUI application for learning vocabulary using flashcards                 ║
# ║  Features:                                                                ║
# ║  - Three modes: Learn New Words (CSV-based), Repeat Unfamiliar Words,      ║
# ║    Repeat Familiar Words                                                  ║
# ║  - Excludes familiar/unfamiliar words from new words mode                 ║
# ║  - Spaced repetition: cycles for ≤50 words, random with no recent repeats  ║
# ║  - Encouragement message every 20 new words learned                       ║
# ║  - Display order toggle (front/back language)                             ║
# ║  - Automatic card flip after 5 seconds                                    ║
# ║  - User-uploaded CSV with custom language names via settings window       ║
# ║  - Switch between saved language pairs with persisted CSV and progress    ║
# ║  Creation Date: July 23, 2025                                            ║
# ║  Last Modified: July 23, 2025                                            ║
# ║  Notes: Requires two-column CSVs; saves progress to language-specific JSONs║
# ║         Persists language configs in data/language_configs.json           ║
# ║         Future: Add support for JSON data loading, GUI enhancements,      ║
# ║         and a dedicated reset function                                    ║
# ╚════════════════════════════════════════════════════════════════════════════╝

import ttkbootstrap as ttk
from PIL import Image, ImageTk
import random
import pandas as pd
import os
import json
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
from collections import deque

BACKGROUND_COLOR = "#B1DDC6"


class FlashCardUI:
    def __init__(self):
        # Initialize window with modern theme
        self.window = ttk.Window(themename="superhero")
        self.window.configure(padx=20, pady=20, background=BACKGROUND_COLOR)
        self.window.title("Flash Cards")
        self.window.geometry("900x800")
        self.window.minsize(800, 600)

        # Initialize language data
        self.languages = {}  # {lang_pair: {"front": str, "back": str, "csv_path": str, "data": list, "words_to_learn": list, "words_learned": list, "learned_count": int, ...}}
        self.current_lang_pair = "Slovenian-English"
        self.languages[self.current_lang_pair] = {
            "front": "Slovenian",
            "back": "English",
            "csv_path": "./data/slovenian_words.csv",
            "data": [],
            "words_to_learn": [],
            "words_learned": [],
            "learned_count": 0,
            "recent_words_new": deque(maxlen=5),
            "recent_words_unfamiliar": deque(maxlen=5),
            "recent_words_learned": deque(maxlen=5),
            "current_word_index_new": 0,
            "current_word_index_unfamiliar": 0,
            "current_word_index_learned": 0
        }
        self.load_language_configs()
        self.load_dictionaries()

        # Initialize display order and learning mode
        self.display_order = self.languages[self.current_lang_pair]["front"]
        self.learning_mode = "new"

        # Load card images
        self.card_front = ImageTk.PhotoImage(Image.open("./images/card_front.png"))
        self.card_back = ImageTk.PhotoImage(Image.open("./images/card_back.png"))

        # Create main frame
        self.main_frame = ttk.Frame(self.window)
        self.main_frame.pack(fill="both", expand=True)

        # Create settings frame
        self.settings_frame = ttk.Frame(self.main_frame)
        self.settings_frame.pack(fill="x", pady=10)

        # Create language selection dropdown
        self.lang_var = ttk.StringVar(value=self.current_lang_pair)
        ttk.Label(self.settings_frame, text="Language:", font=("Arial", 12)).pack(side="left", padx=5)
        self.lang_menu = ttk.OptionMenu(
            self.settings_frame,
            self.lang_var,
            self.current_lang_pair,
            *self.languages.keys(),
            command=self.update_language
        )
        self.lang_menu.pack(side="left", padx=5)

        # Create display order dropdown
        self.order_var = ttk.StringVar(value=self.languages[self.current_lang_pair]["front"])
        ttk.Label(self.settings_frame, text="Display Order:", font=("Arial", 12)).pack(side="left", padx=5)
        self.order_menu = ttk.OptionMenu(
            self.settings_frame,
            self.order_var,
            self.languages[self.current_lang_pair]["front"],
            self.languages[self.current_lang_pair]["front"],
            self.languages[self.current_lang_pair]["back"],
            command=self.update_display_order
        )
        self.order_menu.pack(side="left", padx=5)

        # Create learning mode dropdown
        self.mode_var = ttk.StringVar(value="Learn New Words")
        ttk.Label(self.settings_frame, text="Mode:", font=("Arial", 12)).pack(side="left", padx=5)
        mode_menu = ttk.OptionMenu(
            self.settings_frame,
            self.mode_var,
            "Learn New Words",
            "Learn New Words",
            "Repeat Unfamiliar Words",
            "Repeat Familiar Words",
            command=self.update_learning_mode
        )
        mode_menu.pack(side="left", padx=5)

        # Add settings button
        ttk.Button(self.settings_frame, text="Settings", command=self.open_settings_window).pack(side="left", padx=5)

        # Create canvas for card image
        self.canvas = ttk.Canvas(self.main_frame, width=800, height=526)
        self.canvas.pack(pady=20)

        # Initialize card display (front)
        self.current_side = "front"
        self.card_image_id = self.canvas.create_image(400, 263, image=self.card_front)
        self.title_text_id = self.canvas.create_text(400, 150, text=self.languages[self.current_lang_pair]["front"], font=("Arial", 40, "italic"), fill="black")
        self.word_text_id = self.canvas.create_text(400, 280, text="", font=("Arial", 60, "bold"), fill="black")

        # Display initial random word
        self.current_word = self.get_random_word()
        self.update_card()

        # Create button frame
        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_frame.pack(fill="x", pady=10)

        # Load and process button images
        right_img = Image.open("images/right.png")
        wrong_img = Image.open("images/wrong.png")

        crop_pixels = 5
        def clean_button_image(img):
            width, height = img.size
            crop_box = (crop_pixels, crop_pixels, width - crop_pixels, height - crop_pixels)
            cropped_img = img.crop(crop_box)
            if cropped_img.mode != 'RGBA':
                cropped_img = cropped_img.convert('RGBA')
            from PIL import ImageFilter
            smoothed = cropped_img.filter(ImageFilter.SMOOTH_MORE)
            return smoothed

        right_img_processed = clean_button_image(right_img)
        wrong_img_processed = clean_button_image(wrong_img)
        self.right_image = ImageTk.PhotoImage(right_img_processed)
        self.wrong_image = ImageTk.PhotoImage(wrong_img_processed)

        # Configure button style
        style = ttk.Style()
        style.configure(
            "Borderless.TButton",
            borderwidth=0,
            focuscolor="none",
            padding=0,
            background=BACKGROUND_COLOR,
            relief="flat"
        )
        style.map(
            "Borderless.TButton",
            background=[("active", BACKGROUND_COLOR), ("pressed", BACKGROUND_COLOR)],
            relief=[("pressed", "flat"), ("!pressed", "flat")],
            borderwidth=[("active", 0), ("pressed", 0)]
        )

        # Create canvas buttons
        self.create_canvas_buttons()

    def load_language_configs(self):
        """Load persisted language configurations from language_configs.json."""
        try:
            with open("./data/language_configs.json", "r", encoding='utf-8') as f:
                configs = json.load(f)
            for lang_pair, config in configs.items():
                if os.path.exists(config["csv_path"]):
                    self.languages[lang_pair] = {
                        "front": config["front"],
                        "back": config["back"],
                        "csv_path": config["csv_path"],
                        "data": [],
                        "words_to_learn": [],
                        "words_learned": [],
                        "learned_count": 0,
                        "recent_words_new": deque(maxlen=5),
                        "recent_words_unfamiliar": deque(maxlen=5),
                        "recent_words_learned": deque(maxlen=5),
                        "current_word_index_new": 0,
                        "current_word_index_unfamiliar": 0,
                        "current_word_index_learned": 0
                    }
        except (FileNotFoundError, json.JSONDecodeError):
            # Initialize with default if no config file exists
            pass

    def save_language_configs(self):
        """Save language configurations to language_configs.json."""
        try:
            os.makedirs("./data", exist_ok=True)
            configs = {
                lang_pair: {
                    "front": data["front"],
                    "back": data["back"],
                    "csv_path": data["csv_path"]
                } for lang_pair, data in self.languages.items()
            }
            with open("./data/language_configs.json", "w", encoding='utf-8') as f:
                json.dump(configs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving language configs: {e}")

    def open_settings_window(self):
        """Open a settings window for uploading CSV and setting language names."""
        settings_window = ttk.Toplevel(self.window)
        settings_window.title("Language Settings")
        settings_window.geometry("400x200")
        settings_window.resizable(False, False)

        frame = ttk.Frame(settings_window, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Front Language:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        front_lang_entry = ttk.Entry(frame, width=20)
        front_lang_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Back Language:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        back_lang_entry = ttk.Entry(frame, width=20)
        back_lang_entry.grid(row=1, column=1, padx=5, pady=5)

        def load_csv():
            file_path = filedialog.askopenfilename(
                title="Select CSV File",
                filetypes=[("CSV Files", "*.csv")]
            )
            if not file_path:
                return

            front_lang = front_lang_entry.get().strip()
            back_lang = back_lang_entry.get().strip()
            if not front_lang or not back_lang:
                messagebox.showerror("Error", "Please enter both front and back language names.")
                return

            try:
                data = pd.read_csv(file_path, encoding='utf-8')
                if len(data.columns) != 2:
                    raise ValueError("CSV must have exactly two columns.")
                
                lang_pair = f"{front_lang}-{back_lang}"
                if lang_pair in self.languages:
                    messagebox.showwarning("Warning", f"Language pair {lang_pair} already exists. Overwriting with new CSV.")
                
                data.columns = [front_lang, back_lang]
                self.languages[lang_pair] = {
                    "front": front_lang,
                    "back": back_lang,
                    "csv_path": file_path,
                    "data": data.to_dict(orient="records"),
                    "words_to_learn": [],
                    "words_learned": [],
                    "learned_count": 0,
                    "recent_words_new": deque(maxlen=5),
                    "recent_words_unfamiliar": deque(maxlen=5),
                    "recent_words_learned": deque(maxlen=5),
                    "current_word_index_new": 0,
                    "current_word_index_unfamiliar": 0,
                    "current_word_index_learned": 0
                }
                self.save_dictionaries(lang_pair)
                self.save_language_configs()

                # Update language dropdown
                self.lang_menu['menu'].delete(0, 'end')
                for lp in self.languages.keys():
                    self.lang_menu['menu'].add_command(label=lp, command=lambda x=lp: self.lang_var.set(x))
                self.lang_var.set(lang_pair)
                self.update_language()

                messagebox.showinfo("Success", f"Loaded new language: {lang_pair}")
                settings_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV: {e}")

        ttk.Button(frame, text="Load CSV", command=load_csv).grid(row=2, column=0, columnspan=2, pady=10)

    def load_dictionaries(self):
        """Load or initialize words_to_learn and words_learned dictionaries for the current language."""
        lang_data = self.languages[self.current_lang_pair]
        try:
            data = pd.read_csv(lang_data["csv_path"], encoding='utf-8')
            if len(data.columns) != 2:
                raise ValueError("CSV must have exactly two columns.")
            data.columns = [lang_data["front"], lang_data["back"]]
            lang_data["data"] = data.to_dict(orient="records")

            try:
                with open(f"./data/{self.current_lang_pair}_words_to_learn.json", "r", encoding='utf-8') as f:
                    lang_data["words_to_learn"] = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                lang_data["words_to_learn"] = []

            try:
                with open(f"./data/{self.current_lang_pair}_words_learned.json", "r", encoding='utf-8') as f:
                    lang_data["words_learned"] = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                lang_data["words_learned"] = []

            lang_data["words_to_learn"] = [word for word in lang_data["words_to_learn"] if word in lang_data["data"]]
            lang_data["words_learned"] = [word for word in lang_data["words_learned"] if word in lang_data["data"]]

        except FileNotFoundError:
            print(f"Error: CSV not found at {lang_data['csv_path']} for {self.current_lang_pair}.")
            lang_data["data"] = []
            lang_data["words_to_learn"] = []
            lang_data["words_learned"] = []
        except ValueError as e:
            print(f"Error loading CSV: {e}")
            lang_data["data"] = []
            lang_data["words_to_learn"] = []
            lang_data["words_learned"] = []

    def save_dictionaries(self, lang_pair):
        """Save words_to_learn and words_learned to JSON files for the given language pair."""
        try:
            os.makedirs("./data", exist_ok=True)
            lang_data = self.languages[lang_pair]
            with open(f"./data/{lang_pair}_words_to_learn.json", "w", encoding='utf-8') as f:
                json.dump(lang_data["words_to_learn"], f, ensure_ascii=False, indent=2)
            with open(f"./data/{lang_pair}_words_learned.json", "w", encoding='utf-8') as f:
                json.dump(lang_data["words_learned"], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving dictionaries for {lang_pair}: {e}")

    def update_language(self, *args):
        """Update the current language pair and refresh the UI."""
        self.current_lang_pair = self.lang_var.get()
        self.load_dictionaries()  # Reload CSV and JSON for the selected language
        lang_data = self.languages[self.current_lang_pair]
        self.display_order = lang_data["front"]
        self.order_var.set(lang_data["front"])
        self.order_menu['menu'].delete(0, 'end')
        self.order_menu['menu'].add_command(label=lang_data["front"], command=lambda: self.order_var.set(lang_data["front"]))
        self.order_menu['menu'].add_command(label=lang_data["back"], command=lambda: self.order_var.set(lang_data["back"]))
        self.mode_var.set("Learn New Words")
        self.learning_mode = "new"
        self.current_side = "front"
        self.window.after_cancel(self.flip_timer)
        self.current_word = self.get_random_word()
        self.update_card()

    def get_random_word(self):
        """Return a word dictionary based on learning mode and spaced repetition."""
        lang_data = self.languages[self.current_lang_pair]
        if self.learning_mode == "new":
            available_words = [word for word in lang_data["data"] if word not in lang_data["words_to_learn"] and word not in lang_data["words_learned"]]
            if not available_words:
                available_words = lang_data["data"]
            if len(available_words) <= 50:
                word = available_words[lang_data["current_word_index_new"] % len(available_words)]
                lang_data["current_word_index_new"] += 1
                return word
            else:
                available_words = [word for word in available_words if word not in lang_data["recent_words_new"]]
                if not available_words:
                    lang_data["recent_words_new"].clear()
                    available_words = [word for word in lang_data["data"] if word not in lang_data["words_to_learn"] and word not in lang_data["words_learned"]]
                    if not available_words:
                        available_words = lang_data["data"]
                word = random.choice(available_words)
                lang_data["recent_words_new"].append(word)
                return word
        
        word_list = lang_data["words_to_learn"] if self.learning_mode == "unfamiliar" else lang_data["words_learned"]
        recent_words = lang_data["recent_words_unfamiliar"] if self.learning_mode == "unfamiliar" else lang_data["recent_words_learned"]
        current_index = lang_data["current_word_index_unfamiliar"] if self.learning_mode == "unfamiliar" else lang_data["current_word_index_learned"]

        if not word_list:
            return {lang_data["front"]: "", lang_data["back"]: ""}

        if len(word_list) <= 50:
            word = word_list[current_index]
            if self.learning_mode == "unfamiliar":
                lang_data["current_word_index_unfamiliar"] = (current_index + 1) % len(word_list)
            else:
                lang_data["current_word_index_learned"] = (current_index + 1) % len(word_list)
            return word
        else:
            available_words = [word for word in word_list if word not in recent_words]
            if not available_words:
                recent_words.clear()
                available_words = word_list
            word = random.choice(available_words)
            recent_words.append(word)
            return word

    def update_display_order(self, *args):
        """Update the display order based on user selection and refresh card."""
        self.display_order = self.order_var.get()
        self.current_side = "front"
        self.window.after_cancel(self.flip_timer)
        self.update_card()

    def update_learning_mode(self, *args):
        """Update the learning mode based on user selection and refresh card."""
        selected_mode = self.mode_var.get()
        lang_data = self.languages[self.current_lang_pair]
        if selected_mode == "Repeat Familiar Words" and not lang_data["words_learned"]:
            messagebox.showinfo(
                "No Familiar Words",
                "Go on and learn new words, then come back later to repeat them!"
            )
            self.mode_var.set("Learn New Words")
            self.learning_mode = "new"
        elif selected_mode == "Repeat Unfamiliar Words" and not lang_data["words_to_learn"]:
            messagebox.showinfo(
                "No Unfamiliar Words",
                "Go on and learn new words, then mark some as unfamiliar to repeat them!"
            )
            self.mode_var.set("Learn New Words")
            self.learning_mode = "new"
        else:
            self.learning_mode = {
                "Learn New Words": "new",
                "Repeat Unfamiliar Words": "unfamiliar",
                "Repeat Familiar Words": "familiar"
            }[selected_mode]
            lang_data["current_word_index_new"] = 0
            lang_data["current_word_index_unfamiliar"] = 0
            lang_data["current_word_index_learned"] = 0
            lang_data["recent_words_new"].clear()
            lang_data["recent_words_unfamiliar"].clear()
            lang_data["recent_words_learned"].clear()
        self.current_side = "front"
        self.window.after_cancel(self.flip_timer)
        self.current_word = self.get_random_word()
        self.update_card()

    def update_card(self):
        """Update the canvas to display the current word."""
        lang_data = self.languages[self.current_lang_pair]
        if self.current_side == "front":
            self.canvas.itemconfig(self.card_image_id, image=self.card_front)
            self.canvas.itemconfig(self.title_text_id, text=self.display_order, fill="black")
            self.canvas.itemconfig(self.word_text_id, text=self.current_word[self.display_order], fill="black")
            self.flip_timer = self.window.after(5000, self.flip_to_back)
        else:
            back_language = lang_data["back"] if self.display_order == lang_data["front"] else lang_data["front"]
            self.canvas.itemconfig(self.card_image_id, image=self.card_back)
            self.canvas.itemconfig(self.title_text_id, text=back_language, fill="white")
            self.canvas.itemconfig(self.word_text_id, text=self.current_word[back_language], fill="white")

    def flip_to_back(self):
        """Flip the card to show the opposite language."""
        self.current_side = "back"
        self.update_card()

    def create_canvas_buttons(self):
        self.button_canvas = ttk.Canvas(
            self.btn_frame,
            height=100,
            background=BACKGROUND_COLOR,
            highlightthickness=0
        )
        self.button_canvas.pack(fill="x", pady=10)

        canvas_width = 800
        button_y = 50
        left_button_x = canvas_width // 4
        right_button_x = 3 * canvas_width // 4

        self.wrong_button_id = self.button_canvas.create_image(
            left_button_x, button_y,
            image=self.wrong_image,
            tags="wrong_button"
        )
        self.right_button_id = self.button_canvas.create_image(
            right_button_x, button_y,
            image=self.right_image,
            tags="right_button"
        )

        self.button_canvas.tag_bind("wrong_button", "<Button-1>", lambda e: self.wrong())
        self.button_canvas.tag_bind("right_button", "<Button-1>", lambda e: self.right())
        self.button_canvas.tag_bind("wrong_button", "<Enter>", self.on_wrong_hover)
        self.button_canvas.tag_bind("wrong_button", "<Leave>", self.on_wrong_leave)
        self.button_canvas.tag_bind("right_button", "<Enter>", self.on_right_hover)
        self.button_canvas.tag_bind("right_button", "<Leave>", self.on_right_leave)

    def on_wrong_hover(self, event):
        self.button_canvas.configure(cursor="hand2")

    def on_wrong_leave(self, event):
        self.button_canvas.configure(cursor="")

    def on_right_hover(self, event):
        self.button_canvas.configure(cursor="hand2")

    def on_right_leave(self, event):
        self.button_canvas.configure(cursor="")

    def right(self):
        print("Right button clicked")
        lang_data = self.languages[self.current_lang_pair]
        if self.current_side == "front":
            self.window.after_cancel(self.flip_timer)
            self.flip_to_back()
        else:
            if self.current_word not in lang_data["words_learned"]:
                lang_data["words_learned"].append(self.current_word)
                lang_data["learned_count"] += 1
                if lang_data["learned_count"] % 20 == 0:
                    messagebox.showinfo(
                        "Great Progress!",
                        f"You've learned {lang_data['learned_count']} words! Consider switching to 'Repeat Familiar Words' to review them."
                    )
            if self.current_word in lang_data["words_to_learn"]:
                lang_data["words_to_learn"].remove(self.current_word)
            self.save_dictionaries(self.current_lang_pair)
            self.current_word = self.get_random_word()
            self.current_side = "front"
            self.update_card()

    def wrong(self):
        print("Wrong button clicked")
        lang_data = self.languages[self.current_lang_pair]
        if self.current_side == "front":
            self.window.after_cancel(self.flip_timer)
            self.flip_to_back()
        else:
            if self.current_word not in lang_data["words_to_learn"]:
                lang_data["words_to_learn"].append(self.current_word)
            if self.learning_mode == "familiar" and self.current_word in lang_data["words_learned"]:
                lang_data["words_learned"].remove(self.current_word)
            self.save_dictionaries(self.current_lang_pair)
            self.current_word = self.get_random_word()
            self.current_side = "front"
            self.update_card()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = FlashCardUI()
    app.run()
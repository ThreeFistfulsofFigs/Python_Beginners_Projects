# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                          Password Manager Pro                              ║
# ║  A secure password management application with modern UI using ttkbootstrap║
# ║  Features:                                                                ║
# ║  - AES-256 encryption with Fernet and PBKDF2 key derivation               ║
# ║  - Password generation, storage, viewing, editing, and deletion            ║
# ║  - Import/export passwords as JSON                                        ║
# ║  - Master password protection with local storage                          ║
# ║  - Modern UI with theme switching and context menus                       ║
# ╚════════════════════════════════════════════════════════════════════════════╝

import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import string
import secrets
import json
import os
from datetime import datetime
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class PasswordManager:
    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                     PasswordManager Class                          ║
    # ║ Initializes the application with UI, security, and data attributes  ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def __init__(self):
        # Initialize window with modern theme
        self.window = ttk.Window(themename="superhero")
        self.window.title("🔐 Password Manager Pro")
        self.window.geometry("900x650")
        self.window.minsize(800, 600)

        # Security attributes
        self.cipher_suite = None
        self.data_file = "passwords.json"
        self.config_file = "config.json"
        self.passwords = []

        # Password generation settings
        self.password_length = 12
        self.include_uppercase = True
        self.include_lowercase = True
        self.include_numbers = True
        self.include_symbols = True

        # UI attributes (initialize to None to avoid early access)
        self.stats_label = None
        self.website_entry = None
        self.email_entry = None
        self.password_entry = None
        self.show_pwd_btn = None
        self.search_entry = None
        self.tree = None
        self.context_menu = None
        self.theme_var = None
        self.length_var = None
        self.uppercase_var = None
        self.lowercase_var = None
        self.numbers_var = None
        self.symbols_var = None
        self.notebook = None

        # Load configuration
        self.load_config()

        # Setup UI before loading passwords
        self.setup_ui()

        # Load passwords after UI setup
        self.load_passwords()

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        derive_key                                 ║
    # ║ Derives a secure encryption key from the master password using     ║
    # ║ PBKDF2 with SHA256 and a random salt                              ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        encrypt_data                               ║
    # ║ Encrypts data using Fernet (AES-256) with the derived key          ║
    # ║ Returns a dict with encrypted data and encryption flag             ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def encrypt_data(self, data: str) -> dict:
        if not self.cipher_suite:
            return {"data": data, "encrypted": False}
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return {"data": base64.urlsafe_b64encode(encrypted_data).decode(), "encrypted": True}

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        decrypt_data                               ║
    # ║ Decrypts data using Fernet; handles non-encrypted data and errors  ║
    # ║ Returns decrypted string or empty string on failure                ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def decrypt_data(self, encrypted_dict: dict) -> str:
        if not encrypted_dict.get("encrypted", False):
            return encrypted_dict["data"]
        if not self.cipher_suite:
            messagebox.showerror("Error", "No master password set for decryption!")
            return ""
        try:
            encrypted_data = base64.urlsafe_b64decode(encrypted_dict["data"])
            return self.cipher_suite.decrypt(encrypted_data).decode()
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {e}")
            return ""

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                     setup_master_password                         ║
    # ║ Prompts user to set a master password and generates encryption key ║
    # ║ Saves salt and test string to config file; returns True on success ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def setup_master_password(self):
        password = simpledialog.askstring("🔐 Master Password", "Set your master password:", show='*')
        if not password:
            return False
        salt = os.urandom(16)
        key = self.derive_key(password, salt)
        self.cipher_suite = Fernet(key)
        config = self.load_config()
        config["salt"] = base64.urlsafe_b64encode(salt).decode()
        # Store a test string to verify password later
        test_string = "PasswordManagerTest"
        config["test_string"] = self.encrypt_data(test_string)
        self.save_config(config)
        messagebox.showinfo("✅ Success", "Master password set successfully!")
        return True

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        authenticate                               ║
    # ║ Authenticates user with master password by verifying test string   ║
    # ║ Sets up new password if none exists; returns True on success       ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def authenticate(self):
        config = self.load_config()
        if "salt" not in config or "test_string" not in config:
            return self.setup_master_password()

        for attempt in range(3):  # Allow 3 attempts
            password = simpledialog.askstring("🔐 Authentication", "Enter your master password:", show='*')
            if not password:
                return False
            try:
                salt = base64.urlsafe_b64decode(config["salt"])
                key = self.derive_key(password, salt)
                self.cipher_suite = Fernet(key)
                # Verify password by decrypting test string
                test_string = self.decrypt_data(config["test_string"])
                if test_string == "PasswordManagerTest":
                    return True
                else:
                    messagebox.showerror("❌ Error", f"Invalid master password! {2 - attempt} attempts remaining.")
                    self.cipher_suite = None
            except Exception as e:
                messagebox.showerror("❌ Error", f"Invalid master password! {2 - attempt} attempts remaining.")
                self.cipher_suite = None
        messagebox.showerror("❌ Error", "Too many failed attempts. Exiting.")
        return False

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        load_config                                ║
    # ║ Loads configuration from JSON file; sets default values if missing ║
    # ║ Returns config dictionary                                         ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as file:
                    config = json.load(file)
                    self.password_length = config.get("password_length", 12)
                    self.include_uppercase = config.get("include_uppercase", True)
                    self.include_lowercase = config.get("include_lowercase", True)
                    self.include_numbers = config.get("include_numbers", True)
                    self.include_symbols = config.get("include_symbols", True)
                    return config
            except Exception as e:
                messagebox.showerror("❌ Error", f"Failed to load config: {e}")
        return {}

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        save_config                                ║
    # ║ Saves configuration to JSON file; updates with current settings    ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def save_config(self, config=None):
        if config is None:
            config = {}
        config.update({
            "password_length": self.password_length,
            "include_uppercase": self.include_uppercase,
            "include_lowercase": self.include_lowercase,
            "include_numbers": self.include_numbers,
            "include_symbols": self.include_symbols
        })
        try:
            with open(self.config_file, 'w') as file:
                json.dump(config, file, indent=2)
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to save config: {e}")

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                         setup_ui                                  ║
    # ║ Initializes the main UI with notebook tabs and header              ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def setup_ui(self):
        main_container = ttk.Frame(self.window, padding=10)
        main_container.pack(fill="both", expand=True)

        # Header
        header = ttk.Frame(main_container)
        header.pack(fill="x", pady=(0, 15))
        ttk.Label(header, text="🔐 Password Manager Pro", font=("Segoe UI", 20, "bold")).pack(side="left")
        theme_frame = ttk.Frame(header)
        theme_frame.pack(side="right")
        ttk.Label(theme_frame, text="Theme:", font=("Segoe UI", 10)).pack(side="left", padx=(0, 5))
        self.theme_var = tk.StringVar(value="superhero")
        ttk.Combobox(theme_frame, textvariable=self.theme_var, values=["superhero", "darkly", "cyborg", "vapor"],
                     width=10, state="readonly").pack(side="left")
        self.theme_var.trace("w", self.change_theme)

        # Notebook
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill="both", expand=True)
        self.setup_add_tab()
        self.setup_view_tab()
        self.setup_settings_tab()

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        change_theme                               ║
    # ║ Updates the application theme based on user selection              ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def change_theme(self, *args):
        self.window.style.theme_use(self.theme_var.get())

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        setup_add_tab                              ║
    # ║ Sets up the Add Password tab with input fields and buttons         ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def setup_add_tab(self):
        add_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_frame, text="➕ Add Password")
        container = ttk.Frame(add_frame, padding=20)
        container.pack(fill="both", expand=True)

        # Input card
        card = ttk.LabelFrame(container, text="🆕 New Password", padding=20)
        card.pack(fill="x", pady=(0, 20))

        # Website
        ttk.Label(card, text="🌐 Website:", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.website_entry = ttk.Entry(card, font=("Segoe UI", 11))
        self.website_entry.pack(fill="x", pady=(5, 10))

        # Email
        ttk.Label(card, text="📧 Email/Username:", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.email_entry = ttk.Entry(card, font=("Segoe UI", 11))
        self.email_entry.pack(fill="x", pady=(5, 10))

        # Password
        ttk.Label(card, text="🔑 Password:", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        pwd_frame = ttk.Frame(card)
        pwd_frame.pack(fill="x", pady=(5, 10))
        self.password_entry = ttk.Entry(pwd_frame, font=("Segoe UI", 11), show="*")
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.show_pwd_btn = ttk.Button(pwd_frame, text="👁️", width=3, command=self.toggle_password_visibility)
        self.show_pwd_btn.pack(side="right")

        # Buttons
        btn_frame = ttk.Frame(card)
        btn_frame.pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="🎲 Generate", style="primary.TButton", command=self.generate_password).pack(
            side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="📋 Copy", style="secondary.TButton", command=self.copy_password).pack(side="left",
                                                                                                         padx=(0, 5))
        ttk.Button(btn_frame, text="💾 Save", style="success.TButton", command=self.save_password).pack(side="right")

        # Stats
        stats_card = ttk.LabelFrame(container, text="📊 Stats", padding=10)
        stats_card.pack(fill="x")
        self.stats_label = ttk.Label(stats_card, text="Total passwords: 0", font=("Segoe UI", 10))
        self.stats_label.pack(anchor="w")

        self.website_entry.focus()
        self.window.bind('<Control-g>', lambda e: self.generate_password())
        self.window.bind('<Control-s>', lambda e: self.save_password())

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        setup_view_tab                             ║
    # ║ Sets up the View Passwords tab with search and password list       ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def setup_view_tab(self):
        view_frame = ttk.Frame(self.notebook)
        self.notebook.add(view_frame, text="👁️ View Passwords")
        container = ttk.Frame(view_frame, padding=20)
        container.pack(fill="both", expand=True)

        # Search
        search_card = ttk.LabelFrame(container, text="🔍 Search", padding=10)
        search_card.pack(fill="x", pady=(0, 10))
        search_frame = ttk.Frame(search_card)
        search_frame.pack(fill="x")
        self.search_entry = ttk.Entry(search_frame, font=("Segoe UI", 11))
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.search_entry.bind('<KeyRelease>', self.filter_passwords)
        ttk.Button(search_frame, text="🔄 Refresh", style="secondary.TButton", command=self.refresh_password_list).pack(
            side="right")

        # Password list
        list_card = ttk.LabelFrame(container, text="🗂️ Passwords", padding=10)
        list_card.pack(fill="both", expand=True)
        tree_frame = ttk.Frame(list_card)
        tree_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Custom.Treeview", rowheight=25, font=("Segoe UI", 10))
        style.configure("Custom.Treeview.Heading", font=("Segoe UI", 11, "bold"))

        self.tree = ttk.Treeview(
            tree_frame,
            columns=('Website', 'Email', 'Password', 'Date'),
            show='headings',
            style="Custom.Treeview"
        )
        self.tree.heading('Website', text='🌐 Website')
        self.tree.heading('Email', text='📧 Email/Username')
        self.tree.heading('Password', text='🔑 Password')
        self.tree.heading('Date', text='📅 Added')
        self.tree.column('Website', width=200)
        self.tree.column('Email', width=250)
        self.tree.column('Password', width=150)
        self.tree.column('Date', width=120)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Context menu
        self.context_menu = tk.Menu(self.window, tearoff=0, font=("Segoe UI", 10))
        self.context_menu.add_command(label="📋 Copy Password", command=self.copy_selected_password)
        self.context_menu.add_command(label="📧 Copy Email", command=self.copy_selected_email)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="✏️ Edit", command=self.edit_password)
        self.context_menu.add_command(label="🗑️ Delete", command=self.delete_password)
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Double-1>", self.copy_selected_password)

        self.refresh_password_list()

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                       setup_settings_tab                          ║
    # ║ Sets up the Settings tab for password generation and data management║
    # ╚════════════════════════════════════════════════════════════════════╝
    def setup_settings_tab(self):
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        container = ttk.Frame(settings_frame, padding=20)
        container.pack(fill="both", expand=True)

        # Password generation settings
        gen_card = ttk.LabelFrame(container, text="🎲 Password Generation", padding=20)
        gen_card.pack(fill="x", pady=(0, 10))
        ttk.Label(gen_card, text="🔢 Length:", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.length_var = tk.StringVar(value=str(self.password_length))
        ttk.Spinbox(gen_card, from_=8, to=50, textvariable=self.length_var, width=5, font=("Segoe UI", 11)).pack(
            anchor="w", pady=5)

        ttk.Label(gen_card, text="🔤 Characters:", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(10, 5))
        check_frame = ttk.Frame(gen_card)
        check_frame.pack(fill="x")
        self.uppercase_var = tk.BooleanVar(value=self.include_uppercase)
        self.lowercase_var = tk.BooleanVar(value=self.include_lowercase)
        self.numbers_var = tk.BooleanVar(value=self.include_numbers)
        self.symbols_var = tk.BooleanVar(value=self.include_symbols)
        ttk.Checkbutton(check_frame, text="🔠 Uppercase", variable=self.uppercase_var).pack(side="left", padx=5)
        ttk.Checkbutton(check_frame, text="🔡 Lowercase", variable=self.lowercase_var).pack(side="left", padx=5)
        ttk.Checkbutton(check_frame, text="🔢 Numbers", variable=self.numbers_var).pack(side="left", padx=5)
        ttk.Checkbutton(check_frame, text="🔣 Symbols", variable=self.symbols_var).pack(side="left", padx=5)
        ttk.Button(gen_card, text="💾 Save Settings", style="primary.TButton", command=self.save_settings).pack(
            anchor="w", pady=10)

        # Data management
        data_card = ttk.LabelFrame(container, text="🗄️ Data Management", padding=20)
        data_card.pack(fill="x", pady=(0, 10))
        btn_frame = ttk.Frame(data_card)
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="📤 Export", style="info.TButton", command=self.export_passwords).pack(side="left",
                                                                                                         padx=(0, 5))
        ttk.Button(btn_frame, text="📥 Import", style="info.TButton", command=self.import_passwords).pack(side="left",
                                                                                                         padx=(0, 5))
        ttk.Button(btn_frame, text="🔐 Change Master Password", style="warning.TButton",
                   command=self.change_master_password).pack(side="right")

        # Security info
        security_card = ttk.LabelFrame(container, text="🛡️ Security", padding=10)
        security_card.pack(fill="x")
        ttk.Label(
            security_card,
            text="🔒 AES-256 encryption\n🔑 PBKDF2 with 100,000 iterations\n💾 Local storage only",
            font=("Segoe UI", 10)
        ).pack(anchor="w")

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                    toggle_password_visibility                     ║
    # ║ Toggles visibility of password in the entry field                  ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def toggle_password_visibility(self):
        current_show = self.password_entry.cget("show")
        self.password_entry.config(show="" if current_show == "*" else "*")
        self.show_pwd_btn.config(text="🙈" if current_show == "*" else "👁️")

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                      generate_password                            ║
    # ║ Generates a secure random password based on user settings          ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def generate_password(self):
        self.password_entry.delete(0, "end")
        try:
            length = int(self.length_var.get())
        except ValueError:
            length = 12

        chars = ""
        if self.uppercase_var.get():
            chars += string.ascii_uppercase
        if self.lowercase_var.get():
            chars += string.ascii_lowercase
        if self.numbers_var.get():
            chars += string.digits
        if self.symbols_var.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not chars:
            messagebox.showwarning("⚠️ Warning", "Select at least one character type!")
            return

        password = ''.join(secrets.choice(chars) for _ in range(length))
        self.password_entry.insert(0, password)
        self.password_entry.configure(style="success.TEntry")
        self.window.after(1000, lambda: self.password_entry.configure(style="TEntry"))

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        copy_password                              ║
    # ║ Copies the password from the entry field to the clipboard          ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def copy_password(self):
        password = self.password_entry.get()
        if password:
            self.window.clipboard_clear()
            self.window.clipboard_append(password)
            messagebox.showinfo("✅ Success", "Password copied!")

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        save_password                              ║
    # ║ Saves a new password entry with encryption; handles duplicates     ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def save_password(self):
        website = self.website_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not all([website, email, password]):
            messagebox.showwarning("⚠️ Warning", "Please fill in all fields!")
            return

        for entry in self.passwords:
            if entry.get('website', '').lower() == website.lower():
                if not messagebox.askyesno("🔄 Duplicate", f"Password for {website} exists. Update it?"):
                    return
                self.passwords.remove(entry)
                break

        entry = {
            'website': website,
            'email': email,
            'password': self.encrypt_data(password),
            'date_added': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.passwords.append(entry)
        self.save_passwords()
        messagebox.showinfo("✅ Success", f"Password for {website} saved!")
        self.website_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.website_entry.focus()
        self.update_stats()
        self.refresh_password_list()

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        load_passwords                             ║
    # ║ Loads passwords from JSON file; initializes empty list if none     ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def load_passwords(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    self.passwords = json.load(file)
            except Exception as e:
                messagebox.showerror("❌ Error", f"Failed to load passwords: {e}")
                self.passwords = []
        if self.stats_label:  # Check if UI is initialized
            self.update_stats()
        if self.tree:  # Check if treeview is initialized
            self.refresh_password_list()

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        save_passwords                             ║
    # ║ Saves passwords to JSON file                                      ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def save_passwords(self):
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.passwords, file, indent=2)
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to save passwords: {e}")

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                      refresh_password_list                        ║
    # ║ Refreshes the password list display with alternating row colors    ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def refresh_password_list(self):
        if not self.tree:
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, entry in enumerate(self.passwords):
            decrypted_password = self.decrypt_data(entry['password'])
            masked_password = '●' * min(len(decrypted_password), 12) if decrypted_password else '●●●●●●'
            tags = ('oddrow',) if i % 2 else ('evenrow',)
            self.tree.insert('', 'end', values=(
                entry.get('website', ''),
                entry.get('email', ''),
                masked_password,
                entry.get('date_added', '')
            ), tags=tags)
        self.tree.tag_configure('oddrow', background='#2d3748')
        self.tree.tag_configure('evenrow', background='#1a202c')
        if self.stats_label:
            self.update_stats()

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        filter_passwords                           ║
    # ║ Filters passwords based on case-insensitive search term in website ║
    # ║ or email; updates stats with filtered count                        ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def filter_passwords(self, event=None):
        if not self.tree or not self.search_entry:
            return
        search_term = self.search_entry.get().lower().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)
        filtered_count = 0
        for i, entry in enumerate(self.passwords):
            website = entry.get('website', '').lower()
            email = entry.get('email', '').lower()
            if not search_term or search_term in website or search_term in email:
                decrypted_password = self.decrypt_data(entry['password'])
                masked_password = '●' * min(len(decrypted_password), 12) if decrypted_password else '●●●●●●'
                tags = ('oddrow',) if filtered_count % 2 else ('evenrow',)
                self.tree.insert('', 'end', values=(
                    entry.get('website', ''),
                    entry.get('email', ''),
                    masked_password,
                    entry.get('date_added', '')
                ), tags=tags)
                filtered_count += 1
        self.tree.tag_configure('oddrow', background='#2d3748')
        self.tree.tag_configure('evenrow', background='#1a202c')
        if self.stats_label:
            self.stats_label.config(text=f"Passwords displayed: {filtered_count} of {len(self.passwords)}")

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                       show_context_menu                           ║
    # ║ Displays context menu for password list on right-click             ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def show_context_menu(self, event):
        if not self.tree or not self.context_menu:
            return
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                      copy_selected_password                       ║
    # ║ Copies selected password from list to clipboard                    ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def copy_selected_password(self):
        if not self.tree:
            return
        selection = self.tree.selection()
        if not selection:
            return
        index = self.tree.index(selection[0])
        if index < len(self.passwords):
            decrypted_password = self.decrypt_data(self.passwords[index]['password'])
            if decrypted_password:
                self.window.clipboard_clear()
                self.window.clipboard_append(decrypted_password)
                messagebox.showinfo("✅ Success", "Password copied!")

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                       copy_selected_email                         ║
    # ║ Copies selected email from list to clipboard                       ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def copy_selected_email(self):
        if not self.tree:
            return
        selection = self.tree.selection()
        if not selection:
            return
        values = self.tree.item(selection[0])['values']
        if values and len(values) > 1:
            self.window.clipboard_clear()
            self.window.clipboard_append(values[1])
            messagebox.showinfo("✅ Success", "Email copied!")

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        edit_password                              ║
    # ║ Opens a window to edit the selected password entry                 ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def edit_password(self):
        if not self.tree:
            return
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("⚠️ Warning", "Select a password to edit!")
            return
        index = self.tree.index(selection[0])
        if index >= len(self.passwords):
            return
        entry = self.passwords[index]
        decrypted_password = self.decrypt_data(entry['password'])

        edit_window = tk.Toplevel(self.window)
        edit_window.title("✏️ Edit Password")
        edit_window.geometry("400x300")
        edit_window.transient(self.window)
        edit_window.grab_set()

        ttk.Label(edit_window, text="🌐 Website:", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        website_entry = ttk.Entry(edit_window, font=("Segoe UI", 11))
        website_entry.pack(fill="x", padx=10, pady=5)
        website_entry.insert(0, entry.get('website', ''))

        ttk.Label(edit_window, text="📧 Email/Username:", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10,
                                                                                             pady=5)
        email_entry = ttk.Entry(edit_window, font=("Segoe UI", 11))
        email_entry.pack(fill="x", padx=10, pady=5)
        email_entry.insert(0, entry.get('email', ''))

        ttk.Label(edit_window, text="🔑 Password:", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10, pady=5)
        password_entry = ttk.Entry(edit_window, font=("Segoe UI", 11), show="*")
        password_entry.pack(fill="x", padx=10, pady=5)
        password_entry.insert(0, decrypted_password)

        def save_changes():
            new_website = website_entry.get().strip()
            new_email = email_entry.get().strip()
            new_password = password_entry.get().strip()
            if not all([new_website, new_email, new_password]):
                messagebox.showwarning("⚠️ Warning", "Please fill in all fields!")
                return
            self.passwords[index] = {
                'website': new_website,
                'email': new_email,
                'password': self.encrypt_data(new_password),
                'date_added': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.save_passwords()
            self.refresh_password_list()
            messagebox.showinfo("✅ Success", "Password updated!")
            edit_window.destroy()

        ttk.Button(edit_window, text="💾 Save Changes", style="success.TButton", command=save_changes).pack(pady=20)

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        delete_password                            ║
    # ║ Deletes the selected password after user confirmation              ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def delete_password(self):
        if not self.tree:
            return
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("⚠️ Warning", "Select a password to delete!")
            return
        index = self.tree.index(selection[0])
        if index >= len(self.passwords):
            return
        website = self.passwords[index].get('website', '')
        if messagebox.askyesno("🗑️ Delete", f"Delete password for {website}?"):
            self.passwords.pop(index)
            self.save_passwords()
            self.refresh_password_list()
            self.update_stats()
            messagebox.showinfo("✅ Success", f"Password for {website} deleted!")

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        save_settings                              ║
    # ║ Saves password generation settings to config file                  ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def save_settings(self):
        try:
            self.password_length = int(self.length_var.get())
            self.include_uppercase = self.uppercase_var.get()
            self.include_lowercase = self.lowercase_var.get()
            self.include_numbers = self.numbers_var.get()
            self.include_symbols = self.symbols_var.get()
            if not any([self.include_uppercase, self.include_lowercase, self.include_numbers, self.include_symbols]):
                messagebox.showwarning("⚠️ Warning", "Select at least one character type!")
                return
            self.save_config()
            messagebox.showinfo("✅ Success", "Settings saved!")
        except ValueError:
            messagebox.showerror("❌ Error", "Invalid password length!")

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                       export_passwords                            ║
    # ║ Exports passwords to a JSON file in decrypted form                 ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def export_passwords(self):
        if not self.passwords:
            messagebox.showwarning("⚠️ Warning", "No passwords to export!")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export Passwords"
        )
        if file_path:
            try:
                export_data = [
                    {**entry, 'password': self.decrypt_data(entry['password'])}
                    for entry in self.passwords
                ]
                with open(file_path, 'w') as file:
                    json.dump(export_data, file, indent=2)
                messagebox.showinfo("✅ Success", "Passwords exported!")
            except Exception as e:
                messagebox.showerror("❌ Error", f"Failed to export passwords: {e}")

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                       import_passwords                            ║
    # ║ Imports passwords from a JSON file; encrypts and handles duplicates║
    # ╚════════════════════════════════════════════════════════════════════╝
    def import_passwords(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Import Passwords"
        )
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    imported_data = json.load(file)
                if not isinstance(imported_data, list):
                    messagebox.showerror("❌ Error", "Invalid file format!")
                    return
                imported_count = 0
                for entry in imported_data:
                    if all(key in entry for key in ['website', 'email', 'password']):
                        new_entry = {
                            'website': entry['website'],
                            'email': entry['email'],
                            'password': self.encrypt_data(entry['password']),
                            'date_added': datetime.now().strftime("%Y-%m-%d %H:%M")
                        }
                        existing = next((e for e in self.passwords if e['website'].lower() == entry['website'].lower()),
                                        None)
                        if existing:
                            if messagebox.askyesno("🔄 Duplicate", f"Password for {entry['website']} exists. Replace?"):
                                self.passwords.remove(existing)
                                self.passwords.append(new_entry)
                                imported_count += 1
                        else:
                            self.passwords.append(new_entry)
                            imported_count += 1
                self.save_passwords()
                self.refresh_password_list()
                self.update_stats()
                messagebox.showinfo("✅ Success", f"Imported {imported_count} passwords!")
            except Exception as e:
                messagebox.showerror("❌ Error", f"Failed to import passwords: {e}")

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                     change_master_password                        ║
    # ║ Changes master password and re-encrypts all passwords              ║
    # ║ Updates test string in config file                                ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def change_master_password(self):
        if not messagebox.askyesno("⚠️ Warning", "Changing master password will re-encrypt all passwords. Continue?"):
            return
        new_password = simpledialog.askstring("🔐 New Master Password", "Enter new password:", show='*')
        if not new_password:
            return
        verify_password = simpledialog.askstring("🔐 Verify Password", "Verify new password:", show='*')
        if new_password != verify_password:
            messagebox.showerror("❌ Error", "Passwords do not match!")
            return
        salt = os.urandom(16)
        key = self.derive_key(new_password, salt)
        new_cipher_suite = Fernet(key)
        try:
            new_passwords = []
            for entry in self.passwords:
                decrypted_pwd = self.decrypt_data(entry['password'])
                if not decrypted_pwd:
                    raise Exception("Failed to decrypt existing passwords")
                new_entry = entry.copy()
                new_entry['password'] = {
                    'data': base64.urlsafe_b64encode(new_cipher_suite.encrypt(decrypted_pwd.encode())).decode(),
                    'encrypted': True
                }
                new_passwords.append(new_entry)
            self.passwords = new_passwords
            self.cipher_suite = new_cipher_suite
            config = self.load_config()
            config["salt"] = base64.urlsafe_b64encode(salt).decode()
            config["test_string"] = self.encrypt_data("PasswordManagerTest")
            self.save_config(config)
            self.save_passwords()
            messagebox.showinfo("✅ Success", "Master password changed!")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to change master password: {e}")

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                        update_stats                               ║
    # ║ Updates the stats label with the total number of passwords         ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def update_stats(self):
        if self.stats_label:
            self.stats_label.config(text=f"Total passwords: {len(self.passwords)}")

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                           run                                     ║
    # ║ Runs the application with authentication check                    ║
    # ╚════════════════════════════════════════════════════════════════════╝
    def run(self):
        if self.authenticate():
            self.window.mainloop()
        else:
            self.window.destroy()


# ╔════════════════════════════════════════════════════════════════════╗
# ║                        Main Execution                             ║
# ║ Creates and runs the PasswordManager application                   ║
# ╚════════════════════════════════════════════════════════════════════╝
if __name__ == "__main__":
    app = PasswordManager()
    app.run()
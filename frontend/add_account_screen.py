import base64
import re
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
from backend.password_managment import PasswordManager
from backend.database import PasswordDatabase
from backend.authentication import Authentication

class AddAccountScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Account")
        self.parent = parent

        self.password_data = {}

        self.label_app_name = tk.Label(self, text="App Name:")
        self.label_username = tk.Label(self, text="Username:")
        self.label_password = tk.Label(self, text="Password:")
        self.label_domain = tk.Label(self, text="Domain:")
        self.label_how_strong_is_password = tk.Label(self, text="Strength")

        self.entry_app_name = tk.Entry(self)
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_domain = tk.Entry(self)
        self.entry_strength = tk.Entry(self)

        self.button_add_password = tk.Button(self, text="Add Password", command=self.add_password, bg="purple", fg="white", width=25)
        self.button_add_password.bind("<Enter>", self.on_enter_button)
        self.button_add_password.bind("<Leave>", self.on_leave_button)
        self.button_generate_password = tk.Button(self, text="Generate Strong Password", command=self.generate_password, bg="purple", fg="white", width=25)
        self.button_generate_password.bind("<Enter>", self.on_enter_button)
        self.button_generate_password.bind("<Leave>", self.on_leave_button)

        self.show_password_var = tk.IntVar()
        self.checkbox_show_password = tk.Checkbutton(self, text="Show Password", variable=self.show_password_var, command=self.toggle_password_visibility)

        self.label_app_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_app_name.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.label_username.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_username.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.label_password.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_password.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.label_domain.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry_domain.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.label_how_strong_is_password.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.entry_strength.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.button_add_password.grid(row=5, column=0, columnspan=2, padx=100, pady=10)
        self.button_generate_password.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        self.checkbox_show_password.grid(row=8, column=0, columnspan=2, padx=10, pady=5)
        
        self.button_check_password = tk.Button(self, text="Check Password", command=self.check_password_strength_main, bg="purple", fg="white", width=25)
        self.button_check_password.bind("<Enter>", self.on_enter_button)
        self.button_check_password.bind("<Leave>", self.on_leave_button)
        self.button_check_password.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

    
    def check_password_strength_main(self):
        password = self.entry_password.get()
        if self.check_password_strength(password):
            self.entry_strength.config(bg="green", text="Strong", fg="black")
        else:
            self.entry_strength.config(bg="red", text="Weak", fg="white")


    @staticmethod
    def check_password_strength(password):
        has_uppercase = any(char.isupper() for char in password)
        has_lowercase = any(char.islower() for char in password)
        has_digit = any(char.isdigit() for char in password)
        has_special = re.match(r'[!@#$%^&*(),.?":{}|<>]', password)

        if not has_uppercase or not has_lowercase or not has_digit or not has_special:
            return False
        else:
            return True

    def on_enter_button(self, event):
        event.widget.config(bg="white", fg="purple")

    def on_leave_button(self, event):
        event.widget.config(bg="purple", fg="white")

    def add_password(self):
        app_name = self.entry_app_name.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        domain = self.entry_domain.get()

        if not app_name or not username or not password:
            messagebox.showerror("Error", "App Name, Username, and Password fields are required")
            return

        user_data = Authentication.fetchUserData() # returns tuple of user data
        user_id = user_data[0]
        app_id = PasswordDatabase.check_app_exists(self, app_name, domain, user_id)

        if app_id is None:
            app_id = PasswordDatabase.add_app(self, app_name, domain, user_id)

        master_pass = user_data[2]  
        encoded_salt = user_data[-1]  

        if isinstance(encoded_salt, tuple):
            encoded_salt = encoded_salt[0]  # get first element of tuple

        # Decode the base64 encoded salt
        salt = base64.b64decode(encoded_salt)

        print("pass: ", master_pass, "salt: ", salt)
        print("master_pass type:", type(master_pass))
        print("salt type:", type(salt))

        encryption_key = PasswordManager.derive_key(master_pass, salt)
        password_manager = PasswordManager(encryption_key)
        encrypted_pass = password_manager.encrypt_password(password)

        PasswordDatabase.add_password(self, user_id, app_id, username, encrypted_pass)

        messagebox.showinfo("Success", "Password added successfully")
        self.destroy()

    def generate_password(self):
        strong_password = PasswordManager.generate_strong_password(self, 16)
        self.entry_password.delete(0, tk.END)
        self.entry_password.insert(0, strong_password)


    def toggle_password_visibility(self):
        if self.show_password_var.get() == 1:
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")


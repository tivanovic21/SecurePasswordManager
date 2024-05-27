import tkinter as tk
import re
from tkinter import messagebox
from tkinter import ttk
from backend.authentication import Authentication
from backend.password_managment import PasswordManager
from backend.database import PasswordDatabase

class RegistrationScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.label_how_strong_is_password = tk.Label(self, text="Strength")
        self.label_email = tk.Label(self, text="Email:")
        self.label_password = tk.Label(self, text="Master password:")
        self.label_confirm_password = tk.Label(self, text="Confirm password:")
        self.label_username = tk.Label(self, text="Username:")
        self.entry_strength = tk.Entry(self)


        self.entry_email = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_confirm_password = tk.Entry(self, show="*")
        self.entry_username = tk.Entry(self)


        self.button_register = tk.Button(self, text="Register", command=self.register, bg="purple", fg="white")
        self.button_generate_password = tk.Button(self, text="Generate Password", command=self.generate_password, bg="purple", fg="white")

        self.button_register.bind("<Enter>", self.on_enter_button)
        self.button_register.bind("<Leave>", self.on_leave_button)

        self.button_generate_password.bind("<Enter>", self.on_enter_button)
        self.button_generate_password.bind("<Leave>", self.on_leave_button)

        self.button_register.grid(row=5, columnspan=2, padx=10, pady=10, sticky="nsew")  # Center horizontally
        self.button_generate_password.grid(row=4, columnspan=2, padx=10, pady=5, sticky="nsew")  # Center horizontally

        self.show_password_var = tk.BooleanVar()
        self.show_password_checkbox = tk.Checkbutton(self, text="Show Password", variable=self.show_password_var, command=self.toggle_password_visibility)

        self.label_login = tk.Label(self, text="Existing user? Log in!", fg="purple", cursor="hand2")
        self.label_login.bind("<Button-1>", lambda event: self.parent.show_login_screen())

        self.label_email.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_email.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.label_confirm_password.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_confirm_password.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.label_username.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry_username.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.label_how_strong_is_password.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.entry_strength.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.button_register.grid(row=5, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.button_generate_password.grid(row=6, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.show_password_checkbox.grid(row=1, column=2, padx=5, pady=5)
        self.label_login.grid(row=7, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.button_check_password = tk.Button(self, text="Check Password", command=self.check_password_strength_main, bg="purple", fg="white", width=25)
        self.button_check_password.bind("<Enter>", self.on_enter_button)
        self.button_check_password.bind("<Leave>", self.on_leave_button)
        self.button_check_password.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

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
        has_special = any(re.search(r'[!@#$%^&*(),.?":{}|<>]', char) for char in password)
        if not has_uppercase or not has_lowercase or not has_digit or not has_special:
            return False
        else:
            return True

    def on_enter_button(self, event):
        event.widget.config(bg="white", fg="purple")

    def on_leave_button(self, event):
        event.widget.config(bg="purple", fg="white")

    def register(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()
        username = self.entry_username.get()

        if not email or not password or not confirm_password or not username:
            messagebox.showerror("Error", "All fields are required")
            return
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        else:
            result, message = Authentication.register_user(email, password, username, twoFA=False, twoFA_secret=None, fingerprint=False, salt='')
            if result: 
                PasswordManager.__init__(self, Authentication.hash_password(password))
                self.parent.show_login_screen()
            elif not result:
                messagebox.showerror("Error", message)

    def generate_password(self):
        strong_password = PasswordManager.generate_strong_password(self, 16)
        self.entry_password.delete(0, tk.END)
        self.entry_password.insert(0, strong_password)
        self.entry_confirm_password.delete(0, tk.END)
        self.entry_confirm_password.insert(0, strong_password)

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.entry_password.config(show="")
            self.entry_confirm_password.config(show="")
        else:
            self.entry_password.config(show="*")
            self.entry_confirm_password.config(show="*")

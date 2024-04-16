import tkinter as tk
from tkinter import messagebox
from backend.authentification import Authentication

class LoginScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.label_email = tk.Label(self, text="Email:")
        self.label_password = tk.Label(self, text="Password:")

        self.entry_email = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")

        self.button_login = tk.Button(self, text="Login", command=self.login)

        self.label_register = tk.Label(self, text="New user? Register!", fg="cyan", cursor="hand2")
        self.label_register.bind("<Button-1>", lambda event: self.parent.show_registration_screen())

        self.label_email.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_email.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.button_login.grid(row=2, columnspan=2, padx=10, pady=10)
        self.label_register.grid(row=3, columnspan=2, padx=10, pady=5)

    def login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        if not email or not password:
            messagebox.showerror("Error", "Email and password are required")
            return
        else:
            result = Authentication.login_user(email, password)

            if result: 
                messagebox.showinfo("Login", f"Logged in as {email}")
                self.parent.show_password_managment_screen()
            else:
                messagebox.showerror("Error", "User not found!")

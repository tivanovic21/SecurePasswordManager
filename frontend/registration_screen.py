import tkinter as tk
from tkinter import messagebox
from backend.authentification import Authentication

class RegistrationScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.label_email = tk.Label(self, text="Email:")
        self.label_password = tk.Label(self, text="Password:")
        self.label_firstname = tk.Label(self, text="First name:")
        self.label_lastname = tk.Label(self, text="Last name:")

        self.entry_email = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_firstname = tk.Entry(self)
        self.entry_lastname = tk.Entry(self)

        self.button_register = tk.Button(self, text="Register", command=self.register)

        self.label_login = tk.Label(self, text="Existing user? Log in!", fg="cyan", cursor="hand2")
        self.label_login.bind("<Button-1>", lambda event: self.parent.show_login_screen())

        self.label_email.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_email.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.label_firstname.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_firstname.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.label_lastname.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry_lastname.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.button_register.grid(row=4, columnspan=2, padx=10, pady=10)
        self.label_login.grid(row=5, columnspan=2, padx=10, pady=5)

    def register(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        fname = self.entry_firstname.get()
        lname = self.entry_lastname.get()

        if not email or not password or not fname or not lname:
            messagebox.showerror("Error", "All fields are required")
            return
        else:
            result = Authentication.register_user(email, password, fname, lname, twoFA=False, twoFA_secret=None)

            if result: 
                messagebox.showinfo("Login", f"Registered as {email}")
                self.parent.show_password_managment_screen()
            else:
                messagebox.showerror("Error", "Failed to register the user!")

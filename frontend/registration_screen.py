import tkinter as tk
from tkinter import messagebox

class RegistrationScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.label_email = tk.Label(self, text="Email:")
        self.label_password = tk.Label(self, text="Password:")

        self.entry_email = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")

        self.button_register = tk.Button(self, text="Register", command=self.register)

        self.label_login = tk.Label(self, text="Existing user? Log in!", fg="cyan", cursor="hand2")
        self.label_login.bind("<Button-1>", lambda event: self.parent.show_login_screen())

        self.label_email.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_email.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.button_register.grid(row=2, columnspan=2, padx=10, pady=10)
        self.label_login.grid(row=3, columnspan=2, padx=10, pady=5)

    def register(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        
        # Perform registration (backend logic)
        messagebox.showinfo("Register", f"Registered as {email}")
        self.parent.show_login_screen()

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from backend.database import PasswordDatabase
from backend.password_managment import PasswordManager

class UpdatePasswordScreen(tk.Toplevel):
    def __init__(self, parent, initial_data):
        super().__init__(parent)
        self.title("Update Password")
        self.parent = parent

        # Initial data to populate the fields
        self.initial_data = initial_data

        print("self.initial_data: ", self.initial_data)

        self.app_id = PasswordDatabase.get_app_id(self, self.initial_data[0])
        self.pass_id = PasswordDatabase.get_pass_id(self, {"username": self.initial_data[2], "password": self.initial_data[3]})

        # Create and arrange widgets
        self.label_app_name = tk.Label(self, text="App Name:")
        self.label_username = tk.Label(self, text="Username:")
        self.label_password = tk.Label(self, text="Password:")
        self.label_domain = tk.Label(self, text="Domain:")

        self.entry_app_name = tk.Entry(self)
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_domain = tk.Entry(self)

        self.button_update_password = tk.Button(self, text="Update Password", command=self.update_password)

        self.label_app_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_app_name.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.label_username.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_username.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.label_password.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_password.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.label_domain.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry_domain.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.button_update_password.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.populate_fields()

    def populate_fields(self):
        self.entry_app_name.insert(0, self.initial_data[0])
        self.entry_username.insert(0, self.initial_data[2])
        self.entry_password.insert(0, self.initial_data[3])
        self.entry_domain.insert(0, self.initial_data[1])

    def update_password(self):
        updated_data = {
            "app_id": self.app_id,
            "pass_id": self.pass_id,
            "app_name": self.entry_app_name.get(),
            "domain": self.entry_domain.get(),
            "username": self.entry_username.get(),
            "password": self.entry_password.get()
        }
  
        PasswordDatabase.update_password(self, self.pass_id, updated_data)
        self.destroy()

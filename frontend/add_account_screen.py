import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
from backend.password_managment import PasswordManager

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

        self.entry_app_name = tk.Entry(self)
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_domain = tk.Entry(self)

        self.button_add_password = tk.Button(self, text="Add Password", command=self.add_password)
        self.button_generate_password = tk.Button(self, text="Generate Strong Password", command=self.generate_password)

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

        self.button_add_password.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.button_generate_password.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.checkbox_show_password.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

    def add_password(self):
        app_name = self.entry_app_name.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        domain = self.entry_domain.get()

        if not app_name or not username or not password:
            messagebox.showerror("Error", "App Name, Username, and Password fields are required")
            return
    
        self.password_data = {
            "app_name" : app_name,
            "username" : username,
            "password" : password,
            "domain" : domain
        }

        user_id = 1
        website_id = PasswordManager.check_website_exists(self, app_name, domain, user_id)

        # save to db
        print("---- PRIJE DODAVANJA ----")
        print("user_id: ", user_id, "website_id: ", website_id, "password: ", password)
        PasswordManager.add_password(self, user_id, website_id, password)
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


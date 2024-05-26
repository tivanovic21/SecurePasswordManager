import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from backend.authentication import Authentication
from backend.password_managment import PasswordManager
from frontend.add_account_screen import AddAccountScreen
from frontend.update_password_screen import UpdatePasswordScreen
from backend.database import PasswordDatabase
import base64

class PasswordManagementScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent  

        # Sidebar
        self.sidebar_frame = tk.Frame(self, bg="black")
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")
        
        self.label_user_profile = tk.Label(self.sidebar_frame, text="User Profile", fg="white", cursor="hand2", bg="purple", highlightthickness=1, highlightbackground="black")
        self.label_user_profile.bind("<Button-1>", lambda event: self.parent.show_user_profile_screen())
        self.label_user_profile.bind("<Enter>", self.on_enter_button)
        self.label_user_profile.bind("<Leave>", self.on_leave_button)
        self.label_user_profile.grid(row=0, pady=(20, 10))

        self.button_logout = tk.Button(self.sidebar_frame, text="Logout", command=self.logout, bg="purple", fg="white")
        self.button_logout.bind("<Enter>", self.on_enter_button)
        self.button_logout.bind("<Leave>", self.on_leave_button)
        self.button_logout.grid(row=1, pady=(255, 0))  # Adjust top margin as needed
      
        # Main content
        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        # Search label
        label_search = tk.Label(self.main_frame, text="Search by website name:")
        label_search.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        # Search bar
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_table)
        self.entry_search = tk.Entry(self.main_frame, textvariable=self.search_var)
        self.entry_search.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Treeview widget
        self.tree = ttk.Treeview(self.main_frame, columns=("App Name", "Domain", "Username", "Password"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("App Name", text="App Name")
        self.tree.heading("Domain", text="Domain")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password")
        self.tree.column("#0", width=50)
        self.tree.column("App Name", width=200)
        self.tree.column("Domain", width=150)
        self.tree.column("Username", width=200)
        self.tree.column("Password", width=200)
        self.tree.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=2, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Add button
        self.button_add_account = tk.Button(self.main_frame, text="Add New Account", command=self.add_account, bg="purple", fg="white")
        self.button_add_account.bind("<Enter>", self.on_enter_button)
        self.button_add_account.bind("<Leave>", self.on_leave_button)
        self.button_add_account.grid(row=3, column=0, padx=10, pady=10, sticky="ew")  # Bottom of the table


        # Configure grid weights for proper resizing
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Fetch data
        self.populate_table()

<<<<<<< HEAD

    def on_enter_button(self, event):
        event.widget.config(bg="white", fg="purple")

    def on_leave_button(self, event):
        event.widget.config(bg="purple", fg="white")
=======
    def on_enter_button(button):
        button.config(bg="purple", fg="white")
    def on_leave_button(button):
        button.config(bg="white", fg="black")
>>>>>>> 4d84b218b57d8f4eb8f85e55c47d420551489244

    def logout(self):
        self.parent.show_login_screen()

    def add_account(self):
        add_account_screen = AddAccountScreen(self)
        add_account_screen.grab_set()
        self.wait_window(add_account_screen)
        self.refresh_table()

    def refresh_table(self):
        for child in self.tree.get_children():
            self.tree.item(child, open=False)
            self.tree.selection_remove(child)
            self.tree.detach(child)
        self.populate_table()

    def filter_table(self, *args):
        search_query = self.search_var.get().lower()
        if search_query != "":
            for child in self.tree.get_children():
                app_name = self.tree.item(child)["values"][0].lower()
                if search_query in app_name:
                    self.tree.item(child, open=True)
                    self.tree.selection_set(child)
                else:
                    self.tree.item(child, open=False)
                    self.tree.selection_remove(child)
                    self.tree.detach(child)
        else: 
            self.refresh_table()

    def populate_table(self):
        data = PasswordDatabase.get_user_passwords(self, 1)
        for i, (username, password, app_name, domain) in enumerate(data, start=1):
            item = self.tree.insert("", "end", text=str(i), values=(app_name, domain, username, password))
            self.tree.bind("<Button-2>", self.show_context_menu)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Update Password", command=lambda: self.update_password(item))
        menu.add_command(label="Delete Password", command=lambda: self.delete_password(item))
        menu.add_command(label="Copy Password", command=lambda: self.copy_password(item))

        menu.post(event.x_root, event.y_root)

    def update_password(self, item):
        values = self.tree.item(item, "values")
        update_window = UpdatePasswordScreen(self, values)
        update_window.grab_set()
        self.wait_window(update_window)
        self.refresh_table()

    def delete_password(self, item):
        confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to delete this password?")
        values = self.tree.item(item, "values")
        delete_data = {
            "username": values[2],
            "password": values[3]
        }
        if confirmed:
            password_id = PasswordDatabase.get_pass_id(self, delete_data)
            PasswordDatabase.delete_password(self, password_id)
            self.tree.delete(item)

    def copy_password(self, item):
        values = self.tree.item(item, "values")
        encrypted_password = values[3]

        user_data = Authentication.fetchUserData()  
        master_pass = user_data[2]  
        encoded_salt = user_data[-1]  

        if isinstance(encoded_salt, tuple):
            encoded_salt = encoded_salt[0]  

        salt = base64.b64decode(encoded_salt)

        encryption_key = PasswordManager.derive_key(master_pass, salt)

        password_manager = PasswordManager(encryption_key)

        decrypted_password = password_manager.decrypt_password(encrypted_password)

        self.clipboard_clear()
        self.clipboard_append(decrypted_password)
        messagebox.showinfo("Password Copied", "The password has been copied to your clipboard.")

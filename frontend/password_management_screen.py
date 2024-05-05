import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from backend.authentication import Authentication
from backend.password_managment import PasswordManager
from frontend.add_account_screen import AddAccountScreen
from frontend.update_password_screen import UpdatePasswordScreen
from backend.database import PasswordDatabase

class PasswordManagementScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent  

        # Sidebar
        self.sidebar_frame = tk.Frame(self, bg="gray")
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")
        
        self.label_user_profile = tk.Label(self.sidebar_frame, text="User Profile", fg="cyan", cursor="hand2")
        self.label_user_profile.bind("<Button-1>", lambda event: self.parent.show_user_profile_screen())
        self.label_user_profile.grid(row=0, pady=(20, 10))

        self.button_logout = tk.Button(self.sidebar_frame, text="Logout", command=self.logout)
        self.button_logout.grid(row=1, pady=(0, 20))

        # Main content
        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.button_add_account = tk.Button(self.main_frame, text="Add New Account", command=self.add_account)
        self.button_add_account.grid(row=0, column=0, padx=10, pady=10)

        self.tree = ttk.Treeview(self.main_frame, columns=("App Name", "Domain", "Username", "Password"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("App Name", text="App Name")
        self.tree.heading("Domain", text="Domain")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password")
        self.tree.column("#0", width=50)
        self.tree.column("App Name", width=150)
        self.tree.column("Domain", width=150)
        self.tree.column("Username", width=150)
        self.tree.column("Password", width=150)
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Search bar
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_table)
        self.entry_search = tk.Entry(self.main_frame, textvariable=self.search_var)
        self.entry_search.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Fetch data
        self.populate_table()

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
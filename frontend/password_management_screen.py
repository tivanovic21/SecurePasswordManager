import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from backend.authentication import Authentication
from backend.password_managment import PasswordManager
from frontend.add_account_screen import AddAccountScreen

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

        self.tree = ttk.Treeview(self.main_frame, columns=("App Name", "Username", "Password"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("App Name", text="App Name")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password")
        self.tree.column("#0", width=50)
        self.tree.column("App Name", width=150)
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
        if add_account_screen.password_data:
            password_data = add_account_screen.password_data
            website_name = password_data["app_name"]
            username = password_data["username"]
            password = password_data["password"]
            domain = password_data["domain"]
            user_id = 1

            print("website_name: ", website_name, "username: ", username, "password: ", password, "domain: ", domain, "user_id: ", user_id)

            website_id = self.check_website_exists(website_name, domain, user_id)
            print("website_id: ", website_id)
            if website_id:
                # WEBSITE EXISTS, INSERT INTO PASSWORD TABLE
                PasswordManager.add_password(self, user_id, website_id, password)
            else:
                # INSERT INTO WEBSITE AND INTO PASSWORD TABLE
                website_id = self.insert_into_websites(website_name, domain, user_id)
                if website_id:
                    PasswordManager.add_password(self, user_id, website_id, password)
                else:
                    messagebox.showerror("Error", "Failed to add account")

    def check_website_exists(self, website_name, domain, user_id):
        return PasswordManager.check_website_exists(self, website_name, domain, user_id)

    def insert_into_websites(self, website_name, domain, user_id):
        return PasswordManager.add_website(self, website_name, domain, user_id)

    def filter_table(self, *args):
        search_query = self.search_var.get().lower()
        for child in self.tree.get_children():
            app_name = self.tree.item(child)["values"][0].lower()
            if search_query in app_name:
                self.tree.item(child, open=True)
                self.tree.selection_set(child)
            else:
                self.tree.item(child, open=False)
                self.tree.selection_remove(child)

    def populate_table(self):
        data = PasswordManager.get_user_passwords(self, 1)
        print("data: ", data)
        for i, (password, app_name) in enumerate(data, start=1):
            self.tree.insert("", "end", text=str(i), values=(app_name, "username", password))


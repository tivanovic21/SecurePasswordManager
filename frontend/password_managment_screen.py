import tkinter as tk

class PasswordManagementScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.label_title = tk.Label(self, text="Password Management")
        self.button_logout = tk.Button(self, text="Logout", command=self.logout)

        self.label_title.grid(row=0, columnspan=2, padx=10, pady=10)
        self.button_logout.grid(row=1, columnspan=2, padx=10, pady=10)

    def logout(self):
        # Perform logout logic (if any)
        self.parent.show_login_screen()

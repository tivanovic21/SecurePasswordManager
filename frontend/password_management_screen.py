import tkinter as tk

class PasswordManagementScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.label_user_profile = tk.Label(self, text="User Profile", fg="cyan", cursor="hand2")
        self.label_user_profile.bind("<Button-1>", lambda event: self.parent.show_user_profile_screen())
        self.label_user_profile.grid(row=1, columnspan=2, padx=10, pady=10)

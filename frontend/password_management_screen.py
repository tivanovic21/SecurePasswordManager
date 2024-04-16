import tkinter as tk

class PasswordManagementScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.label_title = tk.Label(self, text='Welcome ' + self.parent.user_data[0] + '!')
        self.button_logout = tk.Button(self, text="Logout", command=self.logout)

        self.label_title.grid(row=0, columnspan=2, padx=10, pady=10)
        self.button_logout.grid(row=1, columnspan=2, padx=10, pady=10)

    def update_user_data(self):
        if self.parent.user_data:
            welcomeText = "Welcome, " + self.parent.user_data[1] + " " + self.parent.user_data[2] + "!"
            self.label_title.config(text=welcomeText)
        else:
            self.label_title.config(text="Welcome! Please log in.")

    def logout(self):
        self.parent.show_login_screen()

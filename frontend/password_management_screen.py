import tkinter as tk
from backend.authentification import Authentication

class PasswordManagementScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.label_title = tk.Label(self, text='Welcome ' + self.parent.user_data[0] + '!')
        self.button_logout = tk.Button(self, text="Logout", command=self.logout)

        self.label_title.grid(row=0, columnspan=2, padx=10, pady=10)
        self.button_logout.grid(row=2, columnspan=2, padx=10, pady=10)

        if Authentication.fetchUserData()[6] == 0:
            self.label_fingerprint = tk.Label(self, text='Fingerprint authentication: Disabled')
            self.button_fingerprint = tk.Button(self, text="Enable", command=self.enable_fingerprint)
            self.label_fingerprint.grid(row=1, columnspan=1, column=1, padx=10, pady=10)
            self.button_fingerprint.grid(row=1, columnspan=1, column=2, padx=10, pady=10)
        else:
            self.label_fingerprint = tk.Label(self, text='Fingerprint authentication: Enabled')
            self.button_fingerprint = tk.Button(self, text="Disable", command=self.disable_fingerprint)
            self.label_fingerprint.grid(row=1, columnspan=1, column=1, padx=10, pady=10)
            self.button_fingerprint.grid(row=1, columnspan=1, column=2, padx=10, pady=10)

    def logout(self):
        self.parent.show_login_screen()

    def enable_fingerprint(self):
        # Enable fingerprint authentication
        pass

    def disable_fingerprint(self):
        # Disable fingerprint authentication
        pass

import tkinter as tk
from backend.biometric_auth import BiometricAuth
from backend.authentification import Authentication

class UserProfileScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.label_title = tk.Label(self, text='Welcome ' + self.parent.user_data + '!')
        self.label_title.grid(row=0, columnspan=2, padx=10, pady=10)

        self.button_logout = tk.Button(self, text="Logout", command=self.logout)
        self.button_logout.grid(row=2, columnspan=2, padx=10, pady=10)

        self.platform = BiometricAuth.checkPlatform
        self.fingerprintStatus = Authentication.fetchUserData()[6]

        if self.fingerprintStatus == 1:
            self.label_fingerprint = tk.Label(self, text='Fingerprint authentication: Enabled')
            self.button_fingerprint = tk.Button(self, text="Disable", command=lambda: self.update_fingerprint(1))
        else:
            self.label_fingerprint = tk.Label(self, text='Fingerprint authentication: Disabled')
            self.button_fingerprint = tk.Button(self, text="Enable", command=lambda: self.update_fingerprint(0))

        self.label_fingerprint.grid(row=1, columnspan=1, column=1, padx=10, pady=10)
        self.button_fingerprint.grid(row=1, columnspan=1, column=2, padx=10, pady=10)

    def logout(self):
        self.parent.show_login_screen()

    def update_fingerprint(self, status):
        Authentication.updateFingerprint(status)
        if status == 0:
            self.label_fingerprint.config(text='Fingerprint authentication: Enabled')
            self.button_fingerprint.config(text='Disable', command=lambda: self.update_fingerprint(1))
        else:
            self.label_fingerprint.config(text='Fingerprint authentication: Disabled')
            self.button_fingerprint.config(text='Enable', command=lambda: self.update_fingerprint(0))

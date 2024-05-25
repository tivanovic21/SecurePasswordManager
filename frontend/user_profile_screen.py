import tkinter as tk
from backend.biometric_auth import BiometricAuth
from backend.authentication import Authentication

class UserProfileScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.label_title = tk.Label(self, text='Welcome ' + self.parent.user_data + '!')
        self.label_title.grid(row=0, columnspan=2, padx=10, pady=10)

        self.platform = BiometricAuth.checkPlatform
        self.fingerprintStatus = Authentication.fetchUserData()[6]
        self.twoFAStatus = Authentication.fetchUserData()[4]

        self.label_2fa_secret = None

        if self.fingerprintStatus == 1:
            self.label_fingerprint = tk.Label(self, text='Fingerprint authentication: Enabled')
            self.button_fingerprint = tk.Button(self, text="Disable", command=lambda: self.update_fingerprint(1))
        else:
            self.label_fingerprint = tk.Label(self, text='Fingerprint authentication: Disabled')
            self.button_fingerprint = tk.Button(self, text="Enable", command=lambda: self.update_fingerprint(0))

        if self.twoFAStatus == 1:
            self.label_2fa = tk.Label(self, text='Two-factor authentication: Enabled')
            self.button_2fa = tk.Button(self, text="Disable", command=lambda: self.update_2fa(1))
        else:
            self.label_2fa = tk.Label(self, text='Two-factor authentication: Disabled')
            self.button_2fa = tk.Button(self, text="Enable", command=lambda: self.update_2fa(0))

        self.label_fingerprint.grid(row=1, columnspan=1, column=1, padx=10, pady=10)
        self.button_fingerprint.grid(row=1, columnspan=1, column=2, padx=10, pady=10)

        self.label_2fa.grid(row=2, columnspan=1, column=1, padx=10, pady=10)
        self.button_2fa.grid(row=2, columnspan=1, column=2, padx=10, pady=10)

    def update_fingerprint(self, status):
        Authentication.updateFingerprint(status)
        if status == 0:
            self.label_fingerprint.config(text='Fingerprint authentication: Enabled')
            self.button_fingerprint.config(text='Disable', command=lambda: self.update_fingerprint(1))
        else:
            self.label_fingerprint.config(text='Fingerprint authentication: Disabled')
            self.button_fingerprint.config(text='Enable', command=lambda: self.update_fingerprint(0))
    
    def update_2fa(self, status):
        firstTime = Authentication.update2FA(status)
        if status == 0:
            self.label_2fa.config(text='Two-factor authentication: Enabled')
            self.button_2fa.config(text='Disable', command=lambda: self.update_2fa(1))
        else: 
            self.label_2fa.config(text='Two-factor authentication: Disabled')
            self.button_2fa.config(text='Enable', command=lambda: self.update_2fa(0))
        
        if firstTime:
            twoFA_secret = Authentication.fetchUserData()[5]
            self.label_2fa_secret = tk.Text(self, height=1, width=30)
            self.label_2fa_secret.insert(tk.END, twoFA_secret)
            self.label_2fa_secret.config(state='disabled')
            self.label_2fa_secret.grid(row=3, columnspan=2, padx=10, pady=10)
        else:
            if self.label_2fa_secret is not None:
                self.label_2fa_secret.destroy()

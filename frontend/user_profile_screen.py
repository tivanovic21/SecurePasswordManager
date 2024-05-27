import tkinter as tk
from backend.biometric_auth import BiometricAuth
from backend.authentication import Authentication

class UserProfileScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.sidebar_frame = tk.Frame(self, bg="black", height=self.winfo_screenheight())
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")

        self.label_user_profile = tk.Label(self.sidebar_frame, text="User Profile", fg="white", cursor="hand2", bg="purple", highlightthickness=1, highlightbackground="black", width=10)
        self.label_user_profile.bind("<Button-1>", lambda event: self.parent.show_user_profile_screen())
        self.label_user_profile.bind("<Enter>", self.on_enter_button)
        self.label_user_profile.bind("<Leave>", self.on_leave_button)
        self.label_user_profile.grid(row=0, pady=(20, 10))

        self.label_password_management = tk.Label(self.sidebar_frame, text="Passwords", fg="white", cursor="hand2", bg="purple", highlightthickness=1, highlightbackground="black", width=10)
        self.label_password_management.bind("<Button-1>", lambda event: self.parent.show_password_management_screen1())
        self.label_password_management.bind("<Enter>", self.on_enter_button)
        self.label_password_management.bind("<Leave>", self.on_leave_button)
        self.label_password_management.grid(row=1, pady=0)

        self.button_logout = tk.Button(self.sidebar_frame, text="Logout", command=self.logout, bg="purple", fg="white")
        self.button_logout.bind("<Enter>", self.on_enter_button)
        self.button_logout.bind("<Leave>", self.on_leave_button)
        self.button_logout.grid(row=2, pady=(230))  # Adjust top margin as needed


        # Main profile area
        self.profile_frame = tk.Frame(self)
        self.profile_frame.grid(row=0, column=1, sticky="nsew")

        self.parent = parent
        self.label_title = tk.Label(self.profile_frame, text='Welcome ' + self.parent.user_data + '!')
        self.label_title.grid(row=0, columnspan=2, padx=10, pady=10)

        self.platform = BiometricAuth.checkPlatform
        self.fingerprintStatus = Authentication.fetchUserData()[6]
        self.twoFAStatus = Authentication.fetchUserData()[4]

        self.label_2fa_secret = None

        if self.fingerprintStatus == 1:
            self.label_fingerprint = tk.Label(self.profile_frame, text='Fingerprint authentication: Enabled', bg="purple", fg="white")
            self.button_fingerprint = tk.Button(self.profile_frame, text="Disable", command=lambda: self.update_fingerprint(1), bg="purple", fg="white")
        else:
            self.label_fingerprint = tk.Label(self.profile_frame, text='Fingerprint authentication: Disabled', bg="white", fg="black")
            self.button_fingerprint = tk.Button(self.profile_frame, text="Enable", command=lambda: self.update_fingerprint(0))

        if self.twoFAStatus == 1:
            self.label_2fa = tk.Label(self.profile_frame, text='Two-factor authentication: Enabled')
            self.button_2fa = tk.Button(self.profile_frame, text="Disable", command=lambda: self.update_2fa(1))
        else:
            self.label_2fa = tk.Label(self.profile_frame, text='Two-factor authentication: Disabled')
            self.button_2fa = tk.Button(self.profile_frame, text="Enable", command=lambda: self.update_2fa(0))

        self.label_fingerprint.grid(row=1, column=0, padx=10, pady=10)
        self.button_fingerprint.grid(row=1, column=1, padx=10, pady=10)

        self.label_2fa.grid(row=2, column=0, padx=10, pady=10)
        self.button_2fa.grid(row=2, column=1, padx=10, pady=10)

    def on_enter_button(self, event):
        event.widget.config(bg="white", fg="purple")

    def on_leave_button(self, event):
        event.widget.config(bg="purple", fg="white")

    def update_fingerprint(self, status):
        Authentication.updateFingerprint(status)
        if status == 0:
            self.label_fingerprint.config(text='Fingerprint authentication: Enabled')
            self.button_fingerprint.config(text='Disable', command=lambda: self.update_fingerprint(1))
        else:
            self.label_fingerprint.config(text='Fingerprint authentication: Disabled')
            self.button_fingerprint.config(text='Enable', command=lambda: self.update_fingerprint(0))

    def logout(self):
        self.parent.show_login_screen()

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

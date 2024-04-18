import tkinter as tk
from tkinter import messagebox, simpledialog
from backend.authentification import Authentication
from backend.biometric_auth import BiometricAuth
from backend.twoFA import TwoFactorAuth

class LoginScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.label_fingerprint = None

        self.label_password = tk.Label(self, text="Master password:")
        self.entry_password = tk.Entry(self, show="*")

        self.button_login = tk.Button(self, text="Login", command=self.login)

        self.label_register = tk.Label(self, text="New user? Register!", fg="cyan", cursor="hand2")
        self.label_register.bind("<Button-1>", lambda event: self.parent.show_registration_screen())

        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.button_login.grid(row=2, columnspan=2, padx=10, pady=10)
        self.label_register.grid(row=3, columnspan=2, padx=10, pady=5)

    def checkFingerprint(self):
        fingerprintStatus = Authentication.fetchUserData()[6]

        if fingerprintStatus == 1:
            platform = BiometricAuth.checkPlatform()

            if platform == 'macOS':
                self.label_fingerprint = tk.Label(self, text='Login using TouchID', fg='red', cursor='hand2')
                self.label_fingerprint.grid(row=4, columnspan=2, padx=10, pady=5)
                self.label_fingerprint.bind("<Button-1>", lambda event: self.biometric_login(platform))
            elif platform == 'windows':
                self.label_fingerprint = tk.Label(self, text='Login using your fingerprint', fg='red', cursor='hand2')
                self.label_fingerprint.grid(row=4, columnspan=2, padx=10, pady=5)
                self.label_fingerprint.bind("<Button-1>", lambda event: self.biometric_login(platform))
        else:
            if self.label_fingerprint is not None:
                self.label_fingerprint.destroy()
                self.label_fingerprint = None

    def biometric_login(self, platform):
        match platform:
            case 'macOS':
                if BiometricAuth.touchID():
                    # If 2FA is on 
                    if self.check2FA():
                        if self.prompt_for_totp():
                            userData = Authentication.fetchUserData()
                            self.parent.set_user_data(userData[3])
                            self.parent.show_password_management_screen()
                    else:
                        userData = Authentication.fetchUserData()
                        self.parent.set_user_data(userData[3])
                        self.parent.show_password_management_screen()
                else:
                    messagebox.showerror("Login Failed", "TouchID authentication failed.")
            case 'windows':
                if BiometricAuth.wbf():
                    # If 2FA is on 
                    if self.check2FA():
                        if self.prompt_for_totp():
                            userData = Authentication.fetchUserData()
                            self.parent.set_user_data(userData[3])
                            self.parent.show_password_management_screen()
                    else:
                        userData = Authentication.fetchUserData()
                        self.parent.set_user_data(userData[3])
                        self.parent.show_password_management_screen()
                else:
                    messagebox.showerror("Login Failed", "Windows fingerprint authentication failed.")

    def login(self):
        password = self.entry_password.get()
        authentication_result, message = Authentication.login_user(password)

        if authentication_result:
            # If 2FA is on 
            if self.check2FA():
                if self.prompt_for_totp():
                    self.parent.set_user_data(message)
                    messagebox.showinfo("Login", f"Welcome back {message}")
                    self.parent.show_password_management_screen() 
            else:
                self.parent.set_user_data(message)
                messagebox.showinfo("Login", f"Welcome back {message}")
                self.parent.show_password_management_screen()
        else:
            messagebox.showerror("Login Failed", message)

    def check2FA(self):
        enabled = Authentication.fetchUserData()[4]
        return enabled

    def prompt_for_totp(self):
        totp_input = simpledialog.askstring("Enter TOTP", "Please enter your TOTP:")
        if totp_input:
            if TwoFactorAuth.verifyToken(Authentication.fetchUserData()[5], totp_input):
                return True
            else:
                messagebox.showerror("Login Failed", "Invalid TOTP. Please try again.")
                self.prompt_for_totp()

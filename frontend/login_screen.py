import tkinter as tk
from tkinter import messagebox, simpledialog
from backend.authentication import Authentication
from backend.biometric_auth import BiometricAuth
from backend.twoFA import TwoFactorAuth
from backend.email import Email

class LoginScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.label_fingerprint = None
        self.fingerprintStatus = None

        self.label_title = tk.Label(self, text="Password Manager", font=("Helvetica", 20, "bold"))
        self.label_title.grid(row=0, column=0, columnspan=2, padx=(300, 300), pady=(20, 10), sticky="nsew")  # Left and right margin of 200

        # Master password label and entry
        self.label_password = tk.Label(self, text="Master password:")
        self.label_password.grid(row=1, column=0, padx=(300, 10), pady=5, sticky="e")  # Left margin of 200

        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.grid(row=1, column=1, padx=(10, 300), pady=(15,5), sticky="w")  # Right margin of 200

        self.button_login = tk.Button(self, text="Login", command=self.login, bg="purple", fg="white", width=5, anchor="center")
        self.button_reset_password = tk.Button(self, text="Reset Password", command=self.resetPassword, bg="purple", fg="white", width=15, anchor="center")

        self.button_login.bind("<Enter>", lambda event: self.button_login.config(bg="purple", fg="white"))
        self.button_login.bind("<Leave>", lambda event: self.button_login.config(bg="white", fg="black"))

        self.button_reset_password.bind("<Enter>", lambda event: self.button_reset_password.config(bg="purple", fg="white"))
        self.button_reset_password.bind("<Leave>", lambda event: self.button_reset_password.config(bg="white", fg="black"))

        self.button_login.grid(row=2, column=0, padx=400, pady=40, columnspan=2, sticky="nsew")  # Center horizontally
        self.button_reset_password.grid(row=3, column=0, padx=400, pady=0, columnspan=2, sticky="nsew")  # Center horizontally

        self.label_register = tk.Label(self, text="New user? Register!", fg="cyan", cursor="hand2")
        self.label_register.bind("<Button-1>", lambda event: self.parent.show_registration_screen())
        self.label_register.grid(row=4, column=0, columnspan=2, padx=(200, 200), pady=(40, 5), sticky="nsew")  # Top margin of 50


        self.label_register = tk.Label(self, text="New user? Register!", fg="purple", cursor="hand2")
        self.label_register.bind("<Button-1>", lambda event: self.parent.show_registration_screen())
        self.label_register.grid(row=4, column=0, columnspan=2, padx=(200, 200), pady=(40, 5), sticky="nsew")  # Top margin of 50

   

    def resetPassword(self):
        email = simpledialog.askstring('Reset Password', 'Please enter your email address:')
        if email:
            Email.sendPasswordResetEmail(email)
            messagebox.showinfo('Password Reset', 'A password reset email has been sent to your email address.')
            self.promptForToken(email)
    
    def promptForToken(self, email):
        token = simpledialog.askstring('Enter Reset Token', 'Please enter the token from the email:')
        if token:
            result = Authentication.checkToken(email, token)
            if result:
                password = simpledialog.askstring('Enter New Password', 'Please enter your new password:')
                if password:
                    Authentication.saveNewPassword(email, password)
                    messagebox.showinfo('Password Reset', 'Your password has been reset successfully.')

    def checkFingerprint(self):
        user_data = Authentication.fetchUserData()
        if user_data is not None:
            self.fingerprintStatus = user_data[6]
            if self.fingerprintStatus is not None:
                if self.fingerprintStatus == 1:
                    platform = BiometricAuth.checkPlatform()
                    if platform == 'macOS':
                        self.label_fingerprint = tk.Label(self, text='Login using TouchID', fg='red', cursor='hand2')
                        self.label_fingerprint.grid(row=4, columnspan=2, padx=10, pady=5)
                        self.label_fingerprint.bind("<Button-1>", lambda event: self.biometricLogin(platform))
                    elif platform == 'windows':
                        self.label_fingerprint = tk.Label(self, text='Login using your fingerprint', fg='red', cursor='hand2')
                        self.label_fingerprint.grid(row=4, columnspan=2, padx=10, pady=5)
                        self.label_fingerprint.bind("<Button-1>", lambda event: self.biometricLogin(platform))
                else:
                    if self.label_fingerprint is not None:
                        self.label_fingerprint.destroy()
                        self.label_fingerprint = None


    #def biometricLogin(self, platform):
      #  match platform:
      #      case 'macOS':
      #          if BiometricAuth.touchID():
       #             # If 2FA is on 
         #           if self.check2FA():
       #                 if self.promptForTOTP():
       #                     userData = Authentication.fetchUserData()
      #                      self.parent.set_user_data(userData[3])
      #                      self.parent.show_password_management_screen()
       #             else:
        #                userData = Authentication.fetchUserData()
         #               self.parent.set_user_data(userData[3])
          #              self.parent.show_password_management_screen()
           ##        messagebox.showerror("Login Failed", "TouchID authentication failed.")
            #case 'windows':
             #   if BiometricAuth.wbf():
              #      # If 2FA is on 
               #     if self.check2FA():
                  #    if self.promptForTOTP():
                 #           userData = Authentication.fetchUserData()
                  #          self.parent.set_user_data(userData[3])
                   #         self.parent.show_password_management_screen()
                #    else:
               #         userData = Authentication.fetchUserData()
              #          self.parent.set_user_data(userData[3])
              #          self.parent.show_password_management_screen()
              #  else:
              #      messagebox.showerror("Login Failed", "Windows fingerprint authentication failed.")

    def login(self):
        password = self.entry_password.get()
        authentication_result, message = Authentication.login_user(password)

        if authentication_result:
            # If 2FA is on 
            if self.check2FA():
                if self.promptForTOTP():
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

    def promptForTOTP(self):
        totp_input = simpledialog.askstring("Enter TOTP", "Please enter your TOTP:")
        if totp_input:
            if TwoFactorAuth.verifyToken(Authentication.fetchUserData()[5], totp_input):
                return True
            else:
                messagebox.showerror("Login Failed", "Invalid TOTP. Please try again.")
                self.promptForTOTP()

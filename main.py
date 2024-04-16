import tkinter as tk
from frontend.login_screen import LoginScreen
from frontend.registration_screen import RegistrationScreen
from frontend.password_management_screen import PasswordManagementScreen

class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.user_data = None

        self.title('Password Manager')
        self.geometry('400x200')

        self.login_screen = LoginScreen(self)
        # self.registration_screen = RegistrationScreen(self)
        # self.password_managment_screen = PasswordManagementScreen(self)
        self.registration_screen = None
        self.password_management_screen = None

        self.show_login_screen()

    def show_login_screen(self):
        if self.registration_screen:
            self.registration_screen.grid_forget()
        if self.password_management_screen:
            self.password_management_screen.grid_forget()
        self.login_screen.grid()

    def show_registration_screen(self):
        self.login_screen.grid_forget()
        if self.password_management_screen:
            self.password_management_screen.grid_forget()
        if not self.registration_screen:
            self.registration_screen = RegistrationScreen(self)
        self.registration_screen.grid()
    
    def show_password_management_screen(self):
        self.login_screen.grid_forget()
        if self.registration_screen:
            self.registration_screen.grid_forget()
        if not self.password_management_screen:
            self.password_management_screen = PasswordManagementScreen(self)
        self.password_management_screen.grid()

    def set_user_data(self, user_data):
        self.user_data = user_data

if __name__ == '__main__':
    app = PasswordManagerApp()
    app.mainloop()
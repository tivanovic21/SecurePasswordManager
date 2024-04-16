import tkinter as tk
from frontend.login_screen import LoginScreen
from frontend.registration_screen import RegistrationScreen
from frontend.password_managment_screen import PasswordManagementScreen

class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Password Manager')
        self.geometry('400x200')

        self.login_screen = LoginScreen(self)
        self.registration_screen = RegistrationScreen(self)
        self.password_managment_screen = PasswordManagementScreen(self)

        self.show_login_screen()

    def show_login_screen(self):
        self.registration_screen.grid_forget()
        self.password_managment_screen.grid_forget()
        self.login_screen.grid()

    def show_registration_screen(self):
        self.login_screen.grid_forget()
        self.password_managment_screen.grid_forget()
        self.registration_screen.grid()
    
    def show_password_managment_screen(self):
        self.login_screen.grid_forget()
        self.registration_screen.grid_forget()
        self.password_managment_screen.grid()

if __name__ == '__main__':
    app = PasswordManagerApp()
    app.mainloop()
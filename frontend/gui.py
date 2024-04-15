import tkinter as tk
import reg_log as rl

def show_login_screen(event=None):
    register_frame.pack_forget()
    login_frame.pack()
    registerLabel.pack()
    registerLabel.bind('<Button-1>', show_register_screen)

def show_register_screen(event):
    login_frame.pack_forget()
    register_frame.pack()
    loginLabel.pack()
    loginLabel.bind('<Button-1>', show_login_screen)

def login_button_click():
    rl.login(entryEmail.get(), entryPassword.get())

def register_button_click():
    rl.register(entryEmail.get(), entryPassword.get(), entryFirstName.get(), entryLastName.get())

def initialize_login_screen():
    show_login_screen()

# GUI
root = tk.Tk()
root.title('Secure Password Manager')
root.geometry('400x400')

login_frame = tk.Frame(root)
register_frame = tk.Frame(root)

# LOGIN FRAME
tk.Label(login_frame, text='Login').pack()
entryEmail = tk.Entry(login_frame)
entryEmail.pack()
entryPassword = tk.Entry(login_frame)
entryPassword.pack()
btnLogin = tk.Button(login_frame, text='Login', command=login_button_click)
btnLogin.pack()
registerLabel = tk.Label(login_frame, text='New user? Register!')

# REGISTER FRAME
tk.Label(register_frame, text='Register').pack()
entryFirstName = tk.Entry(register_frame)
entryFirstName.pack()
entryLastName = tk.Entry(register_frame)
entryLastName.pack()
btnRegister = tk.Button(register_frame, text='Register', command=register_button_click)
btnRegister.pack()
loginLabel = tk.Label(register_frame, text='Already registered? Login!')

# RUN APP
initialize_login_screen()
root.mainloop()

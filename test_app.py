import unittest
from tkinter import Tk, messagebox
from unittest.mock import MagicMock, patch
from frontend.login_screen import LoginScreen
from frontend.password_management_screen import PasswordManagementScreen

class TestLoginScreen(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = LoginScreen(self.root)

        self.app.parent = self
        self.parent = self
        self.show_password_management_screen_called = False

    def show_password_management_screen(self):
        self.show_password_management_screen_called = True

    def mock_showerror(self, title, message):
        self.error_title = title
        self.error_message = message

    # login using correct credentials
    def test_login_valid(self):
        self.app.entry_password.insert(0, "toni")

        self.original_showinfo = messagebox.showinfo
        messagebox.showinfo = lambda title, message: None

        self.set_user_data_called = False
        self.app.parent.set_user_data = lambda data: setattr(self, 'set_user_data_called', True)

        self.show_password_management_screen_called = False
        self.app.parent.show_password_management_screen = self.show_password_management_screen

        self.app.login()

        self.assertTrue(self.set_user_data_called)
        self.assertTrue(self.show_password_management_screen_called)

        messagebox.showinfo = self.original_showinfo

    # login using wrong credentials
    def test_login_invalid(self):
        self.app.entry_password.insert(0, "wrongpassword")

        self.error_title = None
        self.error_message = None

        self.original_showerror = messagebox.showerror
        messagebox.showerror = self.mock_showerror

        self.app.login()

        self.assertEqual(self.error_title, "Login Failed")
        self.assertIn("Invalid", self.error_message)

        messagebox.showerror = self.original_showerror

    def tearDown(self):
        self.root.destroy()

class TestPasswordManagementScreen(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = PasswordManagementScreen(self.root)
        self.app.parent = MagicMock()
        self.app.clipboard_clear = MagicMock()

    def test_initialization(self):
        self.assertIsNotNone(self.app.sidebar_frame)
        self.assertIsNotNone(self.app.main_frame)
        self.assertIsNotNone(self.app.entry_search)
        self.assertIsNotNone(self.app.tree)
        self.assertIsNotNone(self.app.button_add_account)
        self.assertEqual(self.app.sidebar_frame.winfo_children()[0]['text'], "User Profile")
        self.assertEqual(self.app.sidebar_frame.winfo_children()[1]['text'], "Passwords")
        self.assertEqual(self.app.sidebar_frame.winfo_children()[2]['text'], "Logout")

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()

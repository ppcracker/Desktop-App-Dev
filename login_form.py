# login_form.py
#You can log in using either of the two default accounts:
#Username: user1 | Password: pass1
#Username: user2 | Password: pass2



import sqlite3
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginForm(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("Operator Login")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)

        layout.addWidget(self.label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM operator WHERE username = ? AND password = ?", (username, password))
        result = c.fetchone()
        conn.close()

        if result:
            QMessageBox.information(self, "Login Successful", f"Welcome {username}!")
            self.stack.setCurrentIndex(1)  # Switch to Goods Receiving Form
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

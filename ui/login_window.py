from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QCheckBox,
    QFrame,
    QSizePolicy,
    QSpacerItem,
    QGraphicsDropShadowEffect,
)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.SetUpUi()
        self.SetUpStyle()

    def SetUpUi(self):
        self.setWindowTitle("Sign In")
        self.setObjectName("Root")
        self.setMinimumSize(420, 420)

        # --- Root Layout (center content) ---
        rootLayout = QVBoxLayout(self)
        rootLayout.setContentsMargins(24, 24, 24, 24)
        rootLayout.setSpacing(0)

        # Spacer to vertically center
        rootLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # --- Card ---
        self.Card = QFrame()
        self.Card.setObjectName("Card")
        self.Card.setMinimumWidth(360)
        self.Card.setMaximumWidth(420)

        cardShadow = QGraphicsDropShadowEffect(self.Card)
        cardShadow.setBlurRadius(28)
        cardShadow.setOffset(0, 12)
        cardShadow.setColor(Qt.black)
        self.Card.setGraphicsEffect(cardShadow)

        cardLayout = QVBoxLayout(self.Card)
        cardLayout.setContentsMargins(28, 28, 28, 28)
        cardLayout.setSpacing(18)

        # Title
        self.Title = QLabel("Welcome back 👋")
        self.Title.setObjectName("Title")
        self.Title.setAlignment(Qt.AlignHCenter)
        cardLayout.addWidget(self.Title)

        # Subtitle
        self.Subtitle = QLabel("Please sign in to continue")
        self.Subtitle.setObjectName("Subtitle")
        self.Subtitle.setAlignment(Qt.AlignHCenter)
        cardLayout.addWidget(self.Subtitle)

        # Error label (hidden by default)
        self.ErrorLabel = QLabel("")
        self.ErrorLabel.setObjectName("ErrorLabel")
        self.ErrorLabel.setVisible(False)
        cardLayout.addWidget(self.ErrorLabel)

        # Form
        form = QFormLayout()
        form.setContentsMargins(0, 0, 0, 0)
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(12)

        self.UserNameField = QLineEdit()
        self.UserNameField.setPlaceholderText("Username")
        self.UserNameField.setObjectName("LineEdit")
        self.UserNameField.returnPressed.connect(self.OnLogin)

        self.PasswordField = QLineEdit()
        self.PasswordField.setPlaceholderText("Password")
        self.PasswordField.setEchoMode(QLineEdit.Password)
        self.PasswordField.setObjectName("LineEdit")
        self.PasswordField.returnPressed.connect(self.OnLogin)

        # Show/Hide password action
        togglePwdAction = QAction("Show", self.PasswordField)
        togglePwdAction.setCheckable(True)
        togglePwdAction.toggled.connect(self.OnTogglePassword)
        self.PasswordField.addAction(togglePwdAction, QLineEdit.TrailingPosition)

        form.addRow("Username", self.UserNameField)
        form.addRow("Password", self.PasswordField)
        cardLayout.addLayout(form)

        # Buttons
        self.LoginButton = QPushButton("Sign In")
        self.LoginButton.setObjectName("PrimaryButton")
        self.LoginButton.clicked.connect(self.OnLogin)

        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.setObjectName("GhostButton")
        self.CancelButton.clicked.connect(self.close)

        btnRow = QHBoxLayout()
        btnRow.addWidget(self.CancelButton)
        btnRow.addWidget(self.LoginButton)
        cardLayout.addLayout(btnRow)

        rootLayout.addWidget(self.Card, alignment=Qt.AlignHCenter)

        # Spacer bottom
        rootLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Tab order
        self.setTabOrder(self.UserNameField, self.PasswordField)
        self.setTabOrder(self.PasswordField, self.LoginButton)

    def SetUpStyle(self):
        # Minimal dark theme via QSS (no label backgrounds)
        self.setStyleSheet(
            """
            #Root { background: #0f1115; }
            * { color: #eaeaea; font-family: Inter,Segoe UI,Arial; font-size: 14px; }
            QLabel { background: transparent; }
            #Card { background: #1b1f2a; border-radius: 16px; }
            QLabel#Title { font-size: 22px; font-weight: 700; margin-bottom: 2px; }
            QLabel#Subtitle { color: #a0a7b3; font-size: 13px; }
            QLabel#ErrorLabel { color: #ff6b6b; background: rgba(255,107,107,0.08); border: 1px solid rgba(255,107,107,0.35); padding: 8px 10px; border-radius: 10px; }

            QLineEdit#LineEdit {
                background: #0f1320; border: 1px solid #2a3142; border-radius: 10px;
                padding: 10px 12px; selection-background-color: #3a7afe; selection-color: white;
            }
            QLineEdit#LineEdit:focus { border-color: #3a7afe; }
            QLineEdit#LineEdit[echoMode="2"] { letter-spacing: 0.15em; }

            QPushButton#PrimaryButton {
                background: #3a7afe; color: white; border: none; border-radius: 12px; padding: 10px 14px;
            }
            QPushButton#PrimaryButton:hover { background: #2f67d6; }
            QPushButton#PrimaryButton:pressed { background: #2756b3; }

            QPushButton#GhostButton {
                background: transparent; color: #eaeaea; border: 1px solid #2a3142; border-radius: 12px; padding: 10px 14px;
            }
            QPushButton#GhostButton:hover { background: #0f1320; }
            QPushButton#GhostButton:pressed { background: #0a0d16; }
            """
        )

    def OnTogglePassword(self, checked: bool):
        self.PasswordField.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)
        # Update action text
        for action in self.PasswordField.actions():
            if action.text() in ("Show", "Hide"):
                action.setText("Hide" if checked else "Show")
                break

    def ShowError(self, message: str):
        self.ErrorLabel.setText(message)
        self.ErrorLabel.setVisible(True)

    def ClearError(self):
        self.ErrorLabel.clear()
        self.ErrorLabel.setVisible(False)

    def OnLogin(self):
        self.ClearError()
        username = self.UserNameField.text().strip()
        password = self.PasswordField.text()

        if not username or not password:
            self.ShowError("Please enter both username and password.")
            return

        # --- Demo auth check (replace with real logic) ---
        if username.lower() == "admin" and password == "admin":
            self.ErrorLabel.setStyleSheet(self.styleSheet())  # reset style
            self.ErrorLabel.setVisible(False)
            self.setWindowTitle("Signed in ✔")
            self.LoginButton.setText("Continue")
        else:
            self.ShowError("Invalid credentials. Try 'admin' / 'admin' for the demo.")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec())

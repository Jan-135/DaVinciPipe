from __future__ import annotations

import json
import re
import gazu
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QPixmap, QPainter, QPen, QColor
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, QFrame, \
    QFileDialog


class LoginDialog(QDialog):
    def __init__(self, config=None, parent=None, title="Sign In", subtitle="Please sign in to continue"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(360)
        self.setObjectName("Root")

        self.loaded_config = config
        self.loaded_config_path = None
        self.selected_config_path = None

        if config:
            self.loaded_config_path = config.get("__path__", None)

        # Card
        card = QFrame(self)
        card.setObjectName("Card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.addWidget(card)

        c = QVBoxLayout(card)
        c.setContentsMargins(20, 20, 20, 20)
        c.setSpacing(12)

        titleLbl = QLabel("Welcome back 👋", self)
        titleLbl.setObjectName("Title")
        titleLbl.setAlignment(Qt.AlignHCenter)
        subLbl = QLabel(subtitle, self)
        subLbl.setObjectName("Subtitle")
        subLbl.setAlignment(Qt.AlignHCenter)

        c.addWidget(titleLbl)
        c.addWidget(subLbl)

        self.errorLbl = QLabel("", self)
        self.errorLbl.setObjectName("Error")
        self.errorLbl.setVisible(False)
        c.addWidget(self.errorLbl)

        form = QFormLayout()
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(10)

        self.user = QLineEdit(self)
        self.user.setObjectName("LineEdit")
        self.user.setPlaceholderText("Email")
        self.user.returnPressed.connect(self._attemptLogin)

        self.pwd = QLineEdit(self)
        self.pwd.setObjectName("LineEdit")
        self.pwd.setPlaceholderText("Password")
        self.pwd.setEchoMode(QLineEdit.Password)
        self.pwd.returnPressed.connect(self._attemptLogin)

        # Eye toggle
        self.toggleAction = QAction(self._eyeIcon(False), "", self.pwd)
        self.toggleAction.setCheckable(True)
        self.toggleAction.toggled.connect(self._togglePwd)
        self.toggleAction.setToolTip("Show password")
        self.pwd.addAction(self.toggleAction, QLineEdit.TrailingPosition)

        form.addRow("Email", self.user)
        form.addRow("Password", self.pwd)
        c.addLayout(form)

        # CONFIG FILE PICKER
        self.configPath = QLineEdit(self)
        self.configPath.setObjectName("LineEdit")
        self.configPath.setPlaceholderText("Select config JSON file")

        browseBtn = QPushButton("Browse", self)
        browseBtn.clicked.connect(self._pickConfigFile)

        row = QHBoxLayout()
        row.addWidget(self.configPath)
        row.addWidget(browseBtn)

        form.addRow("Config", row)

        btns = QHBoxLayout()
        self.cancelBtn = QPushButton("Cancel", self)
        self.okBtn = QPushButton("Sign In", self)
        self.cancelBtn.clicked.connect(self.reject)
        self.okBtn.clicked.connect(self._attemptLogin)
        btns.addWidget(self.cancelBtn)
        btns.addWidget(self.okBtn)
        c.addLayout(btns)

        # Styles (kurz & clean)
        self.setStyleSheet("""
            #Root { background: #0f1115; }
            * { color: #eaeaea; font-family: Inter, Segoe UI, Arial; font-size: 14px; }
            QLabel { background: transparent; }
            #Card { background: #1b1f2a; border-radius: 14px; }
            QLabel#Title { font-size: 20px; font-weight: 700; }
            QLabel#Subtitle { color: #a0a7b3; font-size: 12px; }
            QLabel#Error { color: #ff6b6b; background: rgba(255,107,107,0.08); border: 1px solid rgba(255,107,107,0.35); padding: 6px 8px; border-radius: 8px; }
            QLineEdit#LineEdit { background: #0f1320; border:1px solid #2a3142; border-radius:10px; padding:10px 12px; }
            QLineEdit#LineEdit:focus { border-color:#3a7afe; }
            QPushButton { border-radius: 10px; padding: 9px 12px; }
            QPushButton:default, QPushButton[text="Sign In"] { background:#3a7afe; color:white; border:none; }
            QPushButton:hover:default, QPushButton[text="Sign In"]:hover { background:#2f67d6; }
            QPushButton[text="Cancel"] { background:transparent; border:1px solid #2a3142; }
            QPushButton[text="Cancel"]:hover { background:#0f1320; }
        """)

    def getConfigPath(self):
        """Return final config path."""

        if self.selected_config_path:
            return self.selected_config_path

        return self.loaded_config_path

    def _pickConfigFile(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Config JSON", "", "JSON Files (*.json)"
        )
        if path:
            self.configPath.setText(path)
            self.selected_config_path = path

    def _showError(self, msg: str):
        self.errorLbl.setText(msg)
        self.errorLbl.setVisible(True)

    def _attemptLogin(self):
        # 1. Config path holen (entweder user-selected oder default)
        config_path = self.getConfigPath()

        print("[INOFO] config_path: ", self.configPath.text())
        print("[INOFO] config_path: ", self.getConfigPath())

        if not config_path:
            self._showError("Please select a config file.")
            return

        # 2. Config laden
        try:
            with open(config_path, "r") as f:
                cfg = json.load(f).get("kitsu", "")
        except Exception as e:
            self._showError(f"Failed to load config: {e}")
            return

        # 3. API URL extrahieren
        api_url = cfg.get("apiUrl", "").strip()
        if not api_url:
            self._showError("Config file is missing 'apiUrl'.")
            return

        # 4. Credentials prüfen
        email = self.user.text().strip()
        pwd = self.pwd.text()

        if not email or not pwd:
            self._showError("Please enter email and password.")
            return

        # 5. Login versuchen
        self.okBtn.setEnabled(False)
        self.cancelBtn.setEnabled(False)

        try:
            gazu.client.set_host(api_url)
            gazu.log_in(email, pwd)

            # Login success
            self._final_config_path = config_path  # speichern
            self._final_api_url = api_url  # speichern

            self.accept()

        except gazu.exception.AuthFailedException:
            self._showError("Invalid email or password.")
            self.pwd.clear()
            self.pwd.setFocus()

        finally:
            self.okBtn.setEnabled(True)
            self.cancelBtn.setEnabled(True)

    # def getFinalConfigPath(self):
    #     return getattr(self, "_final_config_path", None)

    # def getFinalApiUrl(self):
    #     return getattr(self, "_final_api_url", None)

    def _eyeIcon(self, crossed: bool) -> QIcon:
        pix = QPixmap(20, 20)
        pix.fill(Qt.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor("#a0a7b3"));
        pen.setWidth(2)
        p.setPen(pen)
        p.drawEllipse(5, 7, 10, 6)  # eye
        p.drawEllipse(8, 9, 4, 4)  # pupil
        if crossed:
            p.drawLine(4, 6, 16, 16)
        p.end()
        return QIcon(pix)

    def _togglePwd(self, checked: bool):
        self.pwd.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)
        self.toggleAction.setIcon(self._eyeIcon(checked))
        self.toggleAction.setToolTip("Hide password" if checked else "Show password")

    # def getCredentials(self) -> tuple[str, str]:
    #     return self.user.text().strip(), self.pwd.text()


# def _normalizeApiUrl(url: str | None) -> str:
#     if not url:
#         return ""
#     u = url.strip()
#     if not re.match(r"^https?://", u, re.I):
#         u = "http://" + u
#     if not re.search(r"/api/?$", u, re.I):
#         u = u.rstrip("/") + "/api"
#     return u

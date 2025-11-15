from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)


class MainUi(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("LOL")

        self.setWindowTitle("Kitsu Timeline Sync")
        self.setMinimumWidth(420)
        self.setObjectName("Root")

        # --- Root Layout + Card ---

        rootLayout = QVBoxLayout(self)
        rootLayout.setContentsMargins(16, 16, 16, 16)

        self.cardFrame = QFrame(self)
        self.cardFrame.setObjectName("Card")
        rootLayout.addWidget(self.cardFrame)

        cardLayout = QVBoxLayout(self.cardFrame)
        cardLayout.setContentsMargins(20, 20, 20, 20)
        cardLayout.setSpacing(16)

        # --- Header ---

        titleLabel = QLabel("Timeline Control", self)
        titleLabel.setObjectName("Title")
        titleLabel.setAlignment(Qt.AlignHCenter)

        subtitleLabel = QLabel("Manage your Resolve timeline with Kitsu", self)
        subtitleLabel.setObjectName("Subtitle")
        subtitleLabel.setAlignment(Qt.AlignHCenter)

        cardLayout.addWidget(titleLabel)
        cardLayout.addWidget(subtitleLabel)

        # --- Status Label ---

        self.statusLabel = QLabel("Ready.", self)
        self.statusLabel.setObjectName("Status")
        self.statusLabel.setAlignment(Qt.AlignHCenter)
        self.statusLabel.setWordWrap(True)
        cardLayout.addWidget(self.statusLabel)

        # --- Button Groups ---

        # Row 1: Fetch / Update
        rowFetchUpdate = QHBoxLayout()
        rowFetchUpdate.setSpacing(10)

        self.fetchTimelineButton = QPushButton("Fetch Timeline", self)

        self.updateTimelineButton = QPushButton("Update Timeline", self)

        rowFetchUpdate.addWidget(self.fetchTimelineButton)
        rowFetchUpdate.addWidget(self.updateTimelineButton)
        cardLayout.addLayout(rowFetchUpdate)

        # Row 2: Publish / Save Version
        rowPublishSave = QHBoxLayout()
        rowPublishSave.setSpacing(10)

        self.publishTimelineButton = QPushButton("Publish Timeline", self)

        self.saveVersionButton = QPushButton("Save Version", self)

        rowPublishSave.addWidget(self.publishTimelineButton)
        rowPublishSave.addWidget(self.saveVersionButton)
        cardLayout.addLayout(rowPublishSave)

        # --- Footer Hint ---

        footerLabel = QLabel("Buttons are not connected yet – backend coming next.", self)
        footerLabel.setObjectName("Footer")
        footerLabel.setAlignment(Qt.AlignHCenter)
        cardLayout.addWidget(footerLabel)

        # --- Style ---
        self.fetchTimelineButton.setProperty("role", "primary")
        self.updateTimelineButton.setProperty("role", "primary")
        self.publishTimelineButton.setProperty("role", "secondary")
        self.saveVersionButton.setProperty("role", "secondary")

        # --- Signals ---

        self.fetchTimelineButton.clicked.connect(
            lambda: self.setStatus("Fetch Timeline clicked.")
        )
        self.updateTimelineButton.clicked.connect(
            lambda: self.setStatus("Not implemented yet.")
        )
        self.publishTimelineButton.clicked.connect(
            lambda: self.setStatus("Not implemented yet.")
        )
        self.saveVersionButton.clicked.connect(
            lambda: self.setStatus("Not implemented yet.")
        )

    def setStatus(self, message: str) -> None:
        self.statusLabel.setText(message)

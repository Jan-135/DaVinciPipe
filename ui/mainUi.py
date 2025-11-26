from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QApplication
)


class MainUi(QWidget):
    def __init__(self, handle, parent=None):
        super().__init__(parent)

        self.__handle = handle
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

        footerLabel = QLabel("Next feature is coming soon.", self)
        footerLabel.setObjectName("Footer")
        footerLabel.setAlignment(Qt.AlignHCenter)
        cardLayout.addWidget(footerLabel)

        # --- Style ---
        self.fetchTimelineButton.setProperty("role", "primary")
        self.updateTimelineButton.setProperty("role", "secondary")
        self.publishTimelineButton.setProperty("role", "secondary")
        self.saveVersionButton.setProperty("role", "secondary")

        # --- Signals ---

        self.fetchTimelineButton.clicked.connect(
            self.fetchTimelineButtonClicked
        )
        self.updateTimelineButton.clicked.connect(
            self.updateTimelineButtonClicked
        )
        self.publishTimelineButton.clicked.connect(
            lambda: self.setStatus("Coming soon.")
        )
        self.saveVersionButton.clicked.connect(
            lambda: self.setStatus("Coming soon.")
        )

    def setStatus(self, message: str) -> None:
        self.statusLabel.setText(message)

    def fetchTimelineButtonClicked(self):
        self.setStatus("Fetching...")
        QApplication.processEvents()
        self.__handle.importShotCollection()
        self.setStatus("Fetching successful")

    def updateTimelineButtonClicked(self):
        self.setStatus("Updating...")
        QApplication.processEvents()
        self.__handle.updateTimeline()
        self.setStatus("Update successful")

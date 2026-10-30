from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout


class About(QWidget):
    def __init__(self):
        super().__init__()

        self.header = QLabel("About")
        self.header.setObjectName("header")

        layout = QVBoxLayout(self)
        layout.addWidget(self.header)
        layout.addStretch()
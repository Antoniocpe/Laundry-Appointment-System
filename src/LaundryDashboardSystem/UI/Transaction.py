from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout


class Transaction(QWidget):
    def __init__(self):
        super().__init__()

        self.header = QLabel("Transaction")
        self.header.setObjectName("header")

        layout = QVBoxLayout(self)
        layout.addWidget(self.header)
        layout.addStretch()
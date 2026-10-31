import sys
from PyQt6.QtCore import Qt
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
                            QScrollArea, QFrame)

from widget.receipt import Receipt

class Transaction(QWidget):
    def __init__(self):
        super().__init__()

        self.header = QLabel("Transaction")

        scrollable_content = QFrame()
        receipts_layout = QVBoxLayout(scrollable_content)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setWidget(scrollable_content)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.header)
        main_layout.addWidget(scroll_area)

        dates = [["0", "0", "0"], ["1", "1", "1"]]
        self.receipts = []

        for book_day, service_day, receive_day in dates:
            receipt = Receipt(book_day, service_day, receive_day)
            self.receipts.append(receipt)
            receipts_layout.addWidget(receipt)

        receipts_layout.addStretch()

        self.header.setObjectName("header")

        


if __name__ == "__main__":
    app = QApplication(sys.argv)

    base_dir = Path(__file__).resolve().parent.parent
    transaction_qss = base_dir / "styles" / "Transaction_style.qss"

    if transaction_qss.exists():
        app.setStyleSheet(transaction_qss.read_text())

    window = Transaction()
    window.show()
    sys.exit(app.exec())
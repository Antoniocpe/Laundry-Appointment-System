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

        self.receipts = []

        base_dir = Path(__file__).resolve().parent.parent
        data_dir = base_dir / "data"

        if data_dir.exists() and data_dir.is_dir():
            appointment_files = sorted(data_dir.glob("Appointment_*.txt"), reverse=True)

            for file_path in appointment_files:
                try:
                    content = file_path.read_text()
                    
                    data = {}
                    fn, ln = "", ""
                    
                    for line in content.splitlines():
                        if ":" not in line:
                            continue
                        
                        parts = line.split(":", 1)
                        key = parts[0].strip()
                        val = parts[1].strip()

                        if "First Name" in key:
                            fn = val
                        elif "Last Name" in key:
                            ln = val
                        elif "Date of Appointment" in key:
                            data["date"] = val.split("Time:")[0].strip()
    

                    customer_full_name = f"{fn} {ln}".strip() if (fn or ln) else "Valued Customer"
                    appointment_date = data.get("date", "MM/DD/YYYY")

                    
                    receipt = Receipt(
                        book_day=appointment_date, 
                        service_day=appointment_date, 
                        receive_day=appointment_date
                    )
                    
                    receipt.customer_name.setText(customer_full_name)
                    receipt.total_cost.setText("$9999")

                    self.receipts.append(receipt)
                    receipts_layout.addWidget(receipt)

                except Exception as e:
                    print(f"Failed to load transaction file {file_path.name}: {e}")

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
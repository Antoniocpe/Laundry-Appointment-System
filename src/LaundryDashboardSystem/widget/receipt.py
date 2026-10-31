import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QFrame
from PyQt6.QtGui import QIcon, QTransform, QPixmap

from pathlib import Path

class MoreDetails(QWidget):
    def __init__(self, transit_fee=0, service_fee=0, addOns_fee=0):
        super().__init__()

        MoreDetails_header = QLabel("Transaction Details")
        transit_label = QLabel("Transit Fee")
        transit_fee_label = QLabel(f"{transit_fee}")
        transit_fee_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        service_label = QLabel("service Fee")
        service_fee_label = QLabel(f"{service_fee}")
        service_fee_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        AddOns_label = QLabel("Add-ons Fee")
        AddOns_fee_label = QLabel(f"{addOns_fee}")   
        AddOns_fee_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        more_total_fee = QLabel("Total: 0")
        more_total_fee.setAlignment(Qt.AlignmentFlag.AlignRight)

        MoreDetails_layout = QGridLayout(self)

        MoreDetails_layout.addWidget(MoreDetails_header, 0, 0, 1, 2)
        MoreDetails_layout.addWidget(transit_label, 1, 0)
        MoreDetails_layout.addWidget(transit_fee_label, 1, 1)

        MoreDetails_layout.addWidget(service_label, 2, 0)
        MoreDetails_layout.addWidget(service_fee_label, 2, 1)

        MoreDetails_layout.addWidget(AddOns_label, 3, 0)
        MoreDetails_layout.addWidget(AddOns_fee_label, 3, 1)   
            
        MoreDetails_layout.addWidget(more_total_fee, 4, 0, 1, 2)

        MoreDetails_layout.setContentsMargins(0,0,0,0)

        MoreDetails_header.setObjectName("MoreDetails_header")
        more_total_fee.setObjectName("more_total_fee")

class Receipt(QFrame):
    def __init__(self, book_day="MM/DD/YYYY", service_day="MM/DD/YYYY", receive_day="MM/DD/YYYY"):
        super().__init__()
        self.setObjectName("Receipt")

        self.moreDetails = MoreDetails(0, 0, 0)

        self.customer_name = QLabel("Customer")
        self.total_cost = QLabel("0")
        self.total_cost.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.book_date = QLabel(f"Day of Booking: {book_day}")
        self.service_date = QLabel(f"Day of Service: {service_day}")
        self.received_date = QLabel(f"Date Received: {receive_day}")

        self.base_pixmap = None

        self.showDetails_btn = self.make_button("show_btn.png", "showDetails_btn", "More Details")
        self.showDetails_btn.toggled.connect(self.showDetails)
        self.showDetails_btn.toggled.connect(self.rotate_icon)

        receipt_layout = QGridLayout(self)
        receipt_layout.addWidget(self.customer_name, 0, 0)
        receipt_layout.addWidget(self.total_cost, 0, 1)
        receipt_layout.addWidget(self.book_date, 1, 0)
        receipt_layout.addWidget(self.service_date, 2, 0)
        receipt_layout.addWidget(self.received_date, 3, 0)
        receipt_layout.addWidget(self.showDetails_btn, 4, 0)
        receipt_layout.addWidget(self.moreDetails, 5, 0, 1, 2)
        receipt_layout.setRowStretch(6, 1)

        self.moreDetails.setVisible(False)

        self.customer_name.setObjectName("transaction_customer_name")
        self.total_cost.setObjectName("transaction_total_cost")


    def showDetails(self, checked):
        self.moreDetails.setVisible(checked)
        if checked:
            self.showDetails_btn.setText("Less Details")
        else:
            self.showDetails_btn.setText("More Details")

    def make_button(self, icon_file, object_name, label):
        btn = QPushButton(label)
        btn.setCheckable(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        current_file_path = Path(__file__).resolve()
        root_dir = current_file_path.parent
        while root_dir.parent != root_dir and root_dir.name != "LaundryDashboardSystem":
            root_dir = root_dir.parent

        assets_dir = root_dir / "assets" / "Btn icons"
        icon_path = assets_dir / icon_file

        if icon_path.exists():
            self.base_pixmap = QPixmap(str(icon_path))
            btn.setIcon(QIcon(self.base_pixmap))

        btn.setIconSize(QSize(20,20))
        btn.setObjectName(object_name)
        self.set_style_property(btn, "ShowHideBtn", "show_btn")
        return btn

    def rotate_icon(self, checked):
        # Safety check if asset was missing
        if self.base_pixmap is None or self.base_pixmap.isNull():
            return

        angle = 180 if checked else 0 
        
        transform = QTransform().rotate(angle)
        rotated_pixmap = self.base_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
        self.showDetails_btn.setIcon(QIcon(rotated_pixmap))


    def set_style_property(self, widget, name, value):
        widget.setProperty(name, value)
        widget.style().unpolish(widget)
        widget.style().polish(widget)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    base_dir = Path(__file__).resolve().parent
    transaction_qss = base_dir / "styles" / "Transaction_style.qss"

    if transaction_qss.exists():
        app.setStyleSheet(transaction_qss.read_text())

    receipt = Receipt()
    receipt.resize(270, 280)
    receipt.show()
    sys.exit(app.exec())

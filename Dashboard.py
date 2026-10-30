import sys
from PyQt6.QtCore import Qt
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QGridLayout, QPushButton,
                             QVBoxLayout, QScrollArea, QHBoxLayout, QFrame)

from Washer_button import CustomerCard


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        # ----- widgets -----
        self.header = QLabel("Dashboard")
        self.add_appointment_btn = QPushButton("+ Add Appointment")
        self.add_appointment_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_appointment_btn.setFixedSize(200, 40)

        self.inQueue_text = QLabel("Washes in Queue")
        self.total_text = QLabel("Total: 0 / 0")

        self.details_placeholder = QLabel("Select a washer to view details")
        self.details_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.customer_details_name = QLabel("Customer #1")

        # ----- middle -----
        middle_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        washers_info = QVBoxLayout()

        washers_scrollable_layout = QScrollArea()
        washers_scrollable_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        washers_scrollable_layout.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        washers_scrollable_layout.setWidgetResizable(True)
        washers_scrollable_layout.viewport().setStyleSheet("background: transparent; ")

        scrollable_content = QWidget(washers_scrollable_layout)
        washers_scrollable_layout.setWidget(scrollable_content)
        washers_layout = QVBoxLayout(scrollable_content)    # washers text info + customers

        customers_layout = QGridLayout()  # the whole grid of customers
        customers_container = QFrame()
        customers_container.setLayout(customers_layout)

        header_layout.addWidget(self.header)
        header_layout.addWidget(self.add_appointment_btn)

        # testing [NOT FINAL]
        names = ["Customer #1", "Customer #2", "Customer #3", "Customer #4", "Customer #5"]
        for i, name in enumerate(names):
            customers_layout.addWidget(CustomerCard(name), i // 2, i % 2)

        washers_info.addWidget(self.inQueue_text, stretch=0)
        washers_info.addWidget(self.total_text, stretch=0)

        washers_layout.addWidget(customers_container, stretch=1)

        middle_layout.addLayout(header_layout)
        middle_layout.addLayout(washers_info)
        middle_layout.addWidget(washers_scrollable_layout)
        middle_layout.setContentsMargins(11, 11, 11, 11)

        # ----- details (right) -----

        details_container = QFrame()
        details_container.setAttribute( Qt.WidgetAttribute.WA_StyledBackground, True)

        details_layout = QVBoxLayout(details_container)
        details_layout.addWidget(self.details_placeholder)

        # ----- page layout -----
        page_layout = QHBoxLayout(self)
        page_layout.addLayout(middle_layout, stretch=2)
        page_layout.addWidget(details_container, stretch=1)
        page_layout.setContentsMargins(0, 0, 0, 0)

        # ----- object names (used by the QSS) -----
        self.header.setObjectName("header")
        self.add_appointment_btn.setObjectName("addApptBtn")
        self.inQueue_text.setObjectName("inQueue_text")
        self.total_text.setObjectName("total_text")
        customers_container.setObjectName("customers_layout")
        details_container.setObjectName("details_layout")
        self.details_placeholder.setObjectName("details_placeholder")
        washers_scrollable_layout.setObjectName("washers_scrollable_layout")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    qss_file = Path(__file__).with_name("Dashboard_style.qss")
    app.setStyleSheet(qss_file.read_text())
    window = Dashboard()
    window.show()
    sys.exit(app.exec())
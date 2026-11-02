import sys, os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QMainWindow,
                             QGridLayout, QPushButton, QVBoxLayout,
                             QHBoxLayout)

from PyQt6.QtGui import QIcon
from pathlib import Path

# if u put this on the bottom, "if: __name__ = __main__" it works when running this in solo
# python needs to find these files first or else addAppointment won't work.
base_dir = Path(__file__).resolve().parent.parent

if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from widget.checkmark import Checkmark

class successScreen(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        
    # the qss cannot be accessed by addAppointment if its on the very bottom
        successScreen_qss = base_dir / "styles" / "successScreen.qss"
        if successScreen_qss.exists():
            self.setStyleSheet(successScreen_qss.read_text())

        self.setFixedSize(790, 400)
        self.setObjectName("sucessScreen_qss")

        self.main_window = main_window

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        main_container = QWidget()
        main_container.setLayout(main_layout)

        self.setLayout(main_layout)

#======= header ======== start
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0,0,0,0)
        header_container = QWidget()
        header_container.setLayout(header_layout)

        self.header_text = QLabel("Appointment has been successfully booked.")
        self.header_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout.addWidget(self.header_text, stretch=2)
#======= header ======== end

#======= checkmark ======== start

        success_layout = QGridLayout()
        success_layout.setContentsMargins(0, 0, 0, 0)
        success_layout.setSpacing(2)

        success_container = QWidget()
        success_container.setLayout(success_layout)
        

        checkmark_layout = QGridLayout()
        checkmark_layout.setContentsMargins(0, 0, 0, 0)
        checkmark_layout.setSpacing(2)

        checkmark_container = QWidget()
        checkmark_container.setLayout(checkmark_layout)
 
        self.checkmark = Checkmark()

        checkmark_layout.addWidget(self.checkmark, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        self.prcd_dashboard_btn = QPushButton("Proceed to Dashboard")
        self.prcd_dashboard_btn.setFixedSize(220, 35)
        self.prcd_dashboard_btn.setContentsMargins(0, 10, 0, 0)
        self.prcd_dashboard_btn.clicked.connect(self.close_appointment_window)
        self.thank_you_label = QLabel("Thank you for trusting us!")

        success_layout.addWidget(self.prcd_dashboard_btn, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        success_layout.addWidget(self.thank_you_label, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(header_container, stretch=0)
        main_layout.addWidget(checkmark_container,stretch=2)
        main_layout.addWidget(success_container, stretch=0)

#======= object names ======== start

        main_container.setObjectName("main_container")
        header_container.setObjectName("header_layout")
        success_container.setObjectName("success_container")

        self.header_text.setObjectName("header_text")
        self.thank_you_label.setObjectName("thank_you_label")
        
#======= object names ======== end

    def close_appointment_window(self):
        if self.main_window:
            self.main_window.show()
            
         # Close the parent top-level window (addAppointment)
        top_window = self.window()
        if top_window:
             top_window.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = successScreen()
    window.show()
    sys.exit(app.exec())
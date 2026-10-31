import sys, os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QMainWindow,
                             QGridLayout, QPushButton, QVBoxLayout,
                             QHBoxLayout)

from PyQt6.QtGui import QIcon
from pathlib import Path

class successScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 400)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 5, 0, 15)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        main_container = QWidget()
        main_container.setLayout(main_layout)

        self.setCentralWidget(main_container)

#======= header ======== start
        header_layout = QHBoxLayout()
        header_container = QWidget()
        header_container.setLayout(header_layout)

        self.header_text = QLabel("Appointment has been successfully booked.")
        self.header_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout.addWidget(self.header_text, stretch=2)
#======= header ======== end

#======= checkmark ======== start

        success_layout = QGridLayout()
        success_layout.setContentsMargins(0, 0, 0, 0)
        success_layout.setSpacing(0)

        success_container = QWidget()
        success_container.setLayout(success_layout)
 
        self.checkmark = Checkmark()
        self.prcd_dashboard_btn = QPushButton("Proceed to Dashboard")
        self.prcd_dashboard_btn.setFixedSize(220, 35)
        self.thank_you_label = QLabel("Thank you for trusting us!")

        success_layout.addWidget(self.checkmark, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        success_layout.addWidget(self.prcd_dashboard_btn, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        success_layout.addWidget(self.thank_you_label, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(header_container, stretch=0)
        main_layout.addWidget(success_container, stretch=0)

#======= object names ======== start

        main_container.setObjectName("main_container")
        header_container.setObjectName("header_layout")
        success_container.setObjectName("success_container")

        self.header_text.setObjectName("header_text")
        self.thank_you_label.setObjectName("thank_you_label")
        


#======= object names ======== end

#======= signals and event calls ======== start

if __name__ == "__main__":
    app = QApplication(sys.argv)

    base_dir = Path(__file__).resolve().parent.parent
    successScreen_qss = base_dir / "styles" / "successScreen.qss"

    if successScreen_qss.exists():
        app.setStyleSheet(successScreen_qss.read_text())

    # it cant find the widget folder since this .py file is in the widget folder
    # can't use the .parent method above and won't work that way
    if str(base_dir) not in sys.path:
        sys.path.insert(0, str(base_dir))

    # sys.path needs to find the file first before it must be loaded
    from widget.checkmark import Checkmark

    window = successScreen()
    window.show()
    sys.exit(app.exec())
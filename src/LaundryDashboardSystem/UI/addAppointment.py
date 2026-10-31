import sys, os
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QMainWindow,
                             QGridLayout, QPushButton, QVBoxLayout,
                             QHBoxLayout, QFrame, QComboBox, QStackedLayout, QStackedWidget)

from PyQt6.QtGui import QIcon
from pathlib import Path
from Washer_button import CustomerCard


class addAppointment(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Laundry Dashboard System")
        self.setFixedSize(800, 527)


        main_layout = QVBoxLayout()
        main_container = QWidget()
        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

#======= header ======== start
        header_layout = QHBoxLayout()
        header_container = QWidget()
        header_container.setLayout(header_layout)

        self.back_btn = QPushButton()
        back_btn_icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Btn icons/back_btn.png")
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.setIcon(QIcon(back_btn_icon_path))
        self.back_btn.setIconSize(QSize(40,40))
        self.back_btn.setFlat(True)
        self.back_btn.setToolTip("Back")

        self.header_text = QLabel("Book Appointment")
        self.confirm_btn = QPushButton("Confirm")
        self.confirm_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.confirm_btn.setFixedSize(200, 40)
        
        header_layout.addWidget(self.back_btn, stretch=0)
        header_layout.addWidget(self.header_text, stretch=2)
        header_layout.addWidget(self.confirm_btn, stretch=1)


#======= header ======== end

        progress_layout = QHBoxLayout()
        progress_container = QWidget()
        progress_container.setLayout(progress_layout)
        
        inputDetails_layout = QVBoxLayout()
        inputDetails_container = QWidget()
        inputDetails_container.setLayout(inputDetails_layout)

        personalDetails_layout = QGridLayout()
        services_layout = QGridLayout()
        specification_layout = QGridLayout()
        schedule_layout = QGridLayout()

        main_layout.addWidget(header_container, stretch=0)
        main_layout.addWidget(progress_container, stretch=0)
        main_layout.addWidget(inputDetails_container, stretch=2)

        inputDetails_layout.addLayout(personalDetails_layout)
        inputDetails_layout.addLayout(services_layout)
        inputDetails_layout.addLayout(specification_layout)
        inputDetails_layout.addLayout(schedule_layout)

        main_container.setObjectName("main_container")
        header_container.setObjectName("header_layout")
        progress_container.setObjectName("progress_layout")
        inputDetails_container.setObjectName("inputDetails_layout")
        self.back_btn.setObjectName("back_btn")
        self.header_text.setObjectName("header_text")
        self.confirm_btn.setObjectName("confirm_btn")

                                    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    addAppointment_qss = Path(__file__).with_name("addAppointment.qss")
    app.setStyleSheet(addAppointment_qss.read_text())
    window = addAppointment()
    window.show()
    sys.exit(app.exec())
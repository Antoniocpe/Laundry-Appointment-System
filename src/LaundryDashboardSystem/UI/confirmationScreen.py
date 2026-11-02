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

from widget.Line_divider import Line_divider_thingy

class Confirmation(QWidget):
    def __init__(self):
        super().__init__()

        # the qss cannot be accessed by addAppointment if its on the very bottom
        Confirmation_qss = base_dir / "styles" / "confirmationScreen.qss"
        if Confirmation_qss.exists():
                self.setStyleSheet(Confirmation_qss.read_text())

        self.setFixedSize(600, 430)
        self.setObjectName("confirmation_qss")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        main_container = QWidget()
        main_container.setLayout(main_layout)

        frame_layout = QVBoxLayout() 
        frame_layout.addWidget(main_container)
        self.setLayout(frame_layout)

#======= header ======== start

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_container = QWidget()
        header_container.setLayout(header_layout)

        self.header_text = QLabel("Payment Details")
        self.header_text.setContentsMargins(0,0,0,0)
        self.header_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout.addWidget(self.header_text)

#======= header ======== end

#======= line graphic ======== start

        line_divider_layout = QHBoxLayout()
        line_divider_container = QWidget()
        line_divider_container.setLayout(line_divider_layout)

        self.line_divider = Line_divider_thingy()
        line_divider_layout.addWidget(self.line_divider)

#======= line graphic ======== end

#======= contents ======== start

        contents_layout = QGridLayout()
        contents_container = QWidget()
        contents_container.setLayout(contents_layout)

        self.total_cost_label = QLabel("Total Cost:")
        self.total_cost = QLabel("$9999")
        self.name_label = QLabel("Name:")
        self.name = QLabel(" ")       
        self.delivery_option_label = QLabel("Option of Delivery:")
        self.delivery_option = QLabel(" ")
        self.laundry_specification_label= QLabel("Laundry Specifications:")

        self.ls_options_label = QLabel(" ")
        self.ls_options_label2 = QLabel(" ")
        self.ls_options_label3 = QLabel(" ")
        self.ls_options_label4 = QLabel(" ")
        self.ls_options_label5 = QLabel(" ")

        contents_layout.addWidget(self.total_cost_label, 0, 0)
        contents_layout.addWidget(self.total_cost, 0, 1, alignment= Qt.AlignmentFlag.AlignRight)
        contents_layout.addWidget(self.name_label, 1, 0)
        contents_layout.addWidget(self.name, 1, 1, alignment= Qt.AlignmentFlag.AlignRight)
        contents_layout.addWidget(self.delivery_option_label, 2, 0)
        contents_layout.addWidget(self.delivery_option, 2, 1, alignment= Qt.AlignmentFlag.AlignRight)
        contents_layout.addWidget(self.laundry_specification_label, 3, 0)
        contents_layout.addWidget(self.ls_options_label, 4,0)
        contents_layout.addWidget(self.ls_options_label2, 5,0)
        contents_layout.addWidget(self.ls_options_label3, 6,0)
        contents_layout.addWidget(self.ls_options_label4, 7,0)
        contents_layout.addWidget(self.ls_options_label5, 8,0)

#======= contents ======== end

        main_layout.addWidget(header_container)
        main_layout.addWidget(line_divider_container)
        main_layout.addWidget(contents_container)


#======= object names ======== start

        main_container.setObjectName("main_container")
        self.header_text.setObjectName("header_text")
        self.total_cost_label.setProperty("tag", "widgetLabel")
        self.total_cost.setProperty("tag", "placeholderLabel")
        self.name_label.setProperty("tag", "widgetLabel")
        self.name.setProperty("tag", "placeholderLabel")
        self.delivery_option_label.setProperty("tag", "widgetLabel")
        self.delivery_option.setProperty("tag", "placeholderLabel")
        self.laundry_specification_label.setProperty("tag", "widgetLabel")
        self.ls_options_label.setProperty("tag", "placeholderLabel")
        self.ls_options_label2.setProperty("tag", "placeholderLabel")
        self.ls_options_label3.setProperty("tag", "placeholderLabel")
        self.ls_options_label4.setProperty("tag", "placeholderLabel")
        self.ls_options_label5.setProperty("tag", "placeholderLabel")


#======= object names ======== end


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Confirmation()
    window.show()
    sys.exit(app.exec())
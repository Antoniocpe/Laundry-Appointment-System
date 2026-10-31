import sys, os
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QMainWindow,
                             QGridLayout, QPushButton, QVBoxLayout,
                             QHBoxLayout, QStackedWidget, QLineEdit, QRadioButton)

from PyQt6.QtGui import QIcon
from pathlib import Path

class addAppointment(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Laundry Dashboard System")
        self.setFixedSize(800, 625)

        self.form_count = 0

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(2)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

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
        self.confirm_btn.clicked.connect(self.next_step)

        header_layout.addWidget(self.back_btn, stretch=0)
        header_layout.addWidget(self.header_text, stretch=2)
        header_layout.addWidget(self.confirm_btn, stretch=1)

#======= header ======== end


#======= progress ======== start
        progress_layout = QHBoxLayout()
        progress_container = QWidget()
        progress_container.setLayout(progress_layout)

        self.progress_bar = ProgressBar()
        progress_layout.addWidget(self.progress_bar)
#======= progress ======== end

#======= input details ======== start
        inputDetails_layout = QVBoxLayout()
        inputDetails_layout.setContentsMargins(0,0,0,0)
        inputDetails_layout.setSpacing(0)
        
        inputDetails_container = QWidget()
        inputDetails_container.setLayout(inputDetails_layout)

        # this qstackedwidget basically changes the layout that will be used per click of the confirm button
        self.stepbystep_forms = QStackedWidget()
        self.stepbystep_forms.addWidget(inputDetails_container)

#======= personal details ======== start

        personalDetails_layout = QGridLayout()
        personalDetails_layout.setContentsMargins(0,0,0,6)
        personalDetails_layout.setHorizontalSpacing(15)
        personalDetails_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        personalDetails_container = QWidget()
        personalDetails_container.setLayout(personalDetails_layout)

        self.personalDetails_label = QLabel("Personal Details")

        self.first_name_label = QLabel("First Name")
        self.first_name_label.setContentsMargins(10,0,0,0)
        self.first_name = QLineEdit()
        self.first_name.setFixedWidth(250)
        self.first_name.setFixedHeight(28)
        self.first_name.setContentsMargins(10,0,0,0)

        self.last_name_label = QLabel("Last Name")
        self.last_name_label.setContentsMargins(10,0,0,0)
        self.last_name = QLineEdit()
        self.last_name.setFixedWidth(250)
        self.last_name.setFixedHeight(28)
        self.last_name.setContentsMargins(10,0,0,0)

        self.phone_no_label = QLabel("Phone No.")
        self.phone_no_label.setContentsMargins(10,0,0,0)
        self.phone_no = QLineEdit()
        self.phone_no.setFixedWidth(250)
        self.phone_no.setFixedHeight(28)
        self.phone_no.setContentsMargins(10,0,0,0)

        self.email_address_label = QLabel("Email Address")
        self.email_address_label.setContentsMargins(10,0,0,0)
        self.email_address = QLineEdit()
        self.email_address.setFixedWidth(250)
        self.email_address.setFixedHeight(28)
        self.email_address.setContentsMargins(10,0,0,0)

        self.home_address_label = QLabel("Home Address")
        self.home_address_label.setContentsMargins(10,0,0,0)
        self.home_address = QLineEdit()
        self.home_address.setFixedWidth(250)
        self.home_address.setFixedHeight(28)
        self.home_address.setContentsMargins(10,0,0,0)

        personalDetails_layout.addWidget(self.personalDetails_label, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        personalDetails_layout.addWidget(self.first_name_label, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        personalDetails_layout.addWidget(self.last_name_label, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        personalDetails_layout.addWidget(self.phone_no_label, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        personalDetails_layout.addWidget(self.email_address_label, 3, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        personalDetails_layout.addWidget(self.home_address_label, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        personalDetails_layout.addWidget(self.first_name, 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        personalDetails_layout.addWidget(self.last_name, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        personalDetails_layout.addWidget(self.phone_no, 2, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        personalDetails_layout.addWidget(self.email_address, 4, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        personalDetails_layout.addWidget(self.home_address, 4, 1, alignment=Qt.AlignmentFlag.AlignLeft)

#======= personal details ======== end

#======= services ======== start

        services_layout = QGridLayout()
        services_layout.setContentsMargins(0,0,0,0)
        services_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        services_container = QWidget()
        services_container.setLayout(services_layout)

        self.services_label = QLabel("Services")
        self.services_option1 = QRadioButton("Wash-and-Fold")
        self.services_option1.setChecked(True)
        self.services_option2 = QRadioButton("Dry-Cleaning")
        self.services_option3 = QRadioButton("Pressing && Ironing")

        services_layout.addWidget(self.services_label, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        services_layout.addWidget(self.services_option1, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        services_layout.addWidget(self.services_option2, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        services_layout.addWidget(self.services_option3, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

#======= services ======== end

#======= specification ======== start
        specification_layout = QGridLayout()
        specification_layout.setContentsMargins(0,6,0,6)
        specification_layout.setHorizontalSpacing(15)
        specification_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        specification_container = QWidget()
        specification_container.setLayout(specification_layout)

        self.specification_label = QLabel("Laundry Specifications")

        self.weight_laundry_label = QLabel("Weight of Laundry (kg)")
        self.weight_laundry_label.setContentsMargins(10,0,0,0)

        self.weight_laundry = QLineEdit()
        self.weight_laundry.setPlaceholderText("kg")
        self.weight_laundry.setContentsMargins(10,0,0,0)
        self.weight_laundry.setFixedWidth(165)

        self.garment_count_label = QLabel("Count of Garments")
        self.garment_count = QLineEdit()
        self.garment_count.setPlaceholderText("#")
        self.garment_count.setFixedWidth(135)

        self.addons_label = QLabel("Add-ons")
        self.addons_label.setContentsMargins(0,0,0,0)

        addons_layout = QHBoxLayout()
        addons_layout.setContentsMargins(0,6,0,6)

        addons_container = QWidget()
        addons_container.setLayout(addons_layout)

        self.addons_option1 = QRadioButton("Fabric Softener")
        self.addons_option1.setChecked(True)
        self.addons_option2 = QRadioButton("Bleach")
        self.addons_option3 = QRadioButton("Baking Soda")
        self.addons_option4 = QRadioButton("Extra Spin") 

        self.laundry_note_label = QLabel("Note/Additional Requests")
        self.laundry_note = QLineEdit()
        self.laundry_note.setFixedWidth(560)
        self.laundry_note_label.setContentsMargins(10,0,0,0)

        addons_layout.addWidget(self.addons_option1, alignment=Qt.AlignmentFlag.AlignLeft)
        addons_layout.addWidget(self.addons_option2, alignment=Qt.AlignmentFlag.AlignLeft)
        addons_layout.addWidget(self.addons_option3, alignment=Qt.AlignmentFlag.AlignLeft)
        addons_layout.addWidget(self.addons_option4, alignment=Qt.AlignmentFlag.AlignLeft)

        specification_layout.addWidget(self.specification_label, 0, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft) # extra parameters for span or else i wont fix the damn gap
        specification_layout.addWidget(self.weight_laundry_label, 1,0, alignment=Qt.AlignmentFlag.AlignLeft)
        specification_layout.addWidget(self.garment_count_label, 1,1,alignment=Qt.AlignmentFlag.AlignLeft)
        specification_layout.addWidget(self.addons_label, 1,2, alignment=Qt.AlignmentFlag.AlignLeft)
        specification_layout.addWidget(self.laundry_note_label, 3,0, alignment=Qt.AlignmentFlag.AlignLeft)

        specification_layout.addWidget(self.weight_laundry, 2,0, alignment=Qt.AlignmentFlag.AlignLeft)
        specification_layout.addWidget(self.garment_count, 2,1, alignment=Qt.AlignmentFlag.AlignLeft)
        specification_layout.addWidget(addons_container, 2,2, alignment=Qt.AlignmentFlag.AlignLeft)
        specification_layout.addWidget(self.laundry_note, 3,1,1,2, alignment=Qt.AlignmentFlag.AlignLeft) # same idea as specification label

        specification_layout.setColumnMinimumWidth(2, 400) # width of column 2


#======= specification ======== end

#======= schedule ======== start

        schedule_layout = QGridLayout()
        schedule_layout.setContentsMargins(0,6,0,6)
        schedule_layout.setHorizontalSpacing(15)
        schedule_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        schedule_container = QWidget()
        schedule_container.setLayout(schedule_layout)

        self.schedule_label = QLabel("Schedule Pick-Up/Delivery")
        self.priority_btn = QPushButton("Priority\n15~60mins")
        self.priority_btn.setContentsMargins(10,0,0,0)

        self.priority_btn = QPushButton("Priority\n15~60 mins")
        self.priority_btn.setContentsMargins(10,0,0,0)
        self.same_day_btn = QPushButton("Same-Day\n~24 hours")
        self.same_day_btn.setContentsMargins(10,0,0,0)
        self.standard_btn = QPushButton("Standard\n24~ hours")
        self.standard_btn.setContentsMargins(10,0,0,0)

        schedule_layout.addWidget(self.schedule_label, 0,0,1,2, alignment=Qt.AlignmentFlag.AlignLeft)
        schedule_layout.addWidget(self.priority_btn, 1,0, alignment=Qt.AlignmentFlag.AlignLeft)
        schedule_layout.addWidget(self.same_day_btn, 1,1, alignment=Qt.AlignmentFlag.AlignLeft)
        schedule_layout.addWidget(self.standard_btn, 1,2, alignment=Qt.AlignmentFlag.AlignLeft)

#======= schedule ======== end

        main_layout.addWidget(header_container, stretch=0)
        main_layout.addWidget(progress_container, stretch=0)
        main_layout.addWidget(self.stepbystep_forms, stretch=0)

        inputDetails_layout.addWidget(personalDetails_container, stretch=0)
        inputDetails_layout.addWidget(services_container, stretch=0)
        inputDetails_layout.addWidget(specification_container, stretch=0)
        inputDetails_layout.addWidget(schedule_container, stretch=0)


#======= input details ======== end

#======= success screen ======== start

        success_layout = QHBoxLayout()  
        success_container = QWidget()
        success_container.setLayout(success_layout)

        self.success_container = successScreen()
        self.stepbystep_forms.addWidget(self.success_container)    

#======= success screen ======== end

#======= object names ======== start

        main_container.setObjectName("main_container")

        header_container.setObjectName("header_layout")
        self.back_btn.setObjectName("back_btn")
        self.header_text.setObjectName("header_text")
        self.confirm_btn.setObjectName("confirm_btn")

        progress_container.setObjectName("progress_layout")

        inputDetails_container.setObjectName("inputDetails_layout")
        self.personalDetails_label.setProperty("tag","sectionLabel")
        self.first_name_label.setProperty("tag","widgetLabel")
        self.last_name_label.setProperty("tag","widgetLabel")
        self.phone_no_label.setProperty("tag","widgetLabel")
        self.email_address_label.setProperty("tag","widgetLabel")
        self.home_address_label.setProperty("tag","widgetLabel")

        services_container.setObjectName("services_layout")
        self.services_label.setProperty("tag","sectionLabel")

        specification_container.setObjectName("specification_layout")
        self.specification_label.setProperty("tag","sectionLabel")
        self.weight_laundry_label.setProperty("tag", "widgetLabel")
        self.garment_count_label.setProperty("tag", "widgetLabel")
        self.addons_label.setProperty("tag","widgetLabel")
        self.laundry_note_label.setProperty("tag","widgetLabel")

        schedule_container.setObjectName("schedule_layout")
        self.schedule_label.setProperty("tag", "sectionLabel")
        self.priority_btn.setProperty("tag", "schedule_button")
        self.same_day_btn.setProperty("tag", "schedule_button")
        self.standard_btn.setProperty("tag", "schedule_button")

#======= object names ======== end

#======= signals and event calls ======== start

    def next_step(self):
        self.progress_bar.confirm_step()
        self.form_count +=1
        self.stepbystep_forms.setCurrentIndex(self.form_count)  

#======= signals and event calls ======== end

if __name__ == "__main__":
    app = QApplication(sys.argv)

    base_dir = Path(__file__).resolve().parent.parent
    addappointment_qss = base_dir / "styles" / "addAppointment.qss"

    if addappointment_qss.exists():
       app.setStyleSheet(addappointment_qss.read_text())

    # it cant find the widget folder since this .py file is in the widget folder
    # can't use the .parent method above and won't work that way
    if str(base_dir) not in sys.path:
        sys.path.insert(0, str(base_dir))

    # sys.path needs to find the file first before it must be loaded
    from widget.Progress_bar import ProgressBar
    from successScreen import successScreen


    window = addAppointment()
    window.show()
    sys.exit(app.exec())
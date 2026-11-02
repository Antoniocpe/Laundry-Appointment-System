import sys, os
from PyQt6.QtCore import Qt, QSize, QDateTime, QRegularExpression, pyqtSignal #NEW
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QMainWindow,
                             QGridLayout, QPushButton, QVBoxLayout,QHBoxLayout, 
                             QStackedWidget, QLineEdit, QRadioButton, QCheckBox, 
                             QButtonGroup, QMessageBox)

from PyQt6.QtGui import QIcon, QRegularExpressionValidator
from pathlib import Path

# it cant find the widget folder since this .py file is in the widget folder
# can't use the .parent method above and won't work that way
base_dir = Path(__file__).resolve().parent.parent
if str(base_dir) not in sys.path:
        sys.path.insert(0, str(base_dir))

# sys.path needs to find the file first before it must be loaded
from widget.Progress_bar import ProgressBar
from UI.successScreen import successScreen
from UI.confirmationScreen import Confirmation

class addAppointment(QMainWindow):
    appointment_saved = pyqtSignal(dict) #NEW
    def __init__(self, main_window=None):
        super().__init__()

        self.main_window = main_window

        # the qss cannot be accessed by addAppointment if its on the very bottom
        addappointment_qss = base_dir / "styles" / "addAppointment.qss"
        if addappointment_qss.exists():
                self.setStyleSheet(addappointment_qss.read_text())   

        self.setWindowTitle("Laundry Dashboard System")
        self.setFixedSize(800, 625)
        self.setObjectName("addappointment_qss")
        
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
        back_btn_icon_path = os.path.join(base_dir, "assets", "Btn icons", "back_btn.png")
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.setIcon(QIcon(back_btn_icon_path))
        self.back_btn.setIconSize(QSize(40,40))
        self.back_btn.setFlat(True)
        self.back_btn.setToolTip("Back")
        self.back_btn.clicked.connect(self.close_appointment_window)

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

        characters_only = QRegularExpression("^[a-zA-Z\\s]*$")
        numbers_only = QRegularExpression("^[0-9\\+\\-\\s]*$")
        red_asterisk = "<span style='color: red;'>*</span>"   #an alternative is another qlabel but that will take
                                                              #alot of time by creating another container and adjust layouts and such
                                                              #html attributes can be use on QLabel

        personalDetails_layout = QGridLayout()
        personalDetails_layout.setContentsMargins(0,0,0,6)
        personalDetails_layout.setHorizontalSpacing(15)
        personalDetails_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        personalDetails_container = QWidget()
        personalDetails_container.setLayout(personalDetails_layout)

        self.personalDetails_label = QLabel("Personal Details")

        self.first_name_label = QLabel(f"First Name{red_asterisk}")
        self.first_name_label.setContentsMargins(10,0,0,0)
        self.first_name = QLineEdit()
        self.first_name.setFixedWidth(250)
        self.first_name.setFixedHeight(28)
        self.first_name.setContentsMargins(10,0,0,0)
        self.first_name.setValidator(QRegularExpressionValidator(characters_only, self))

        self.last_name_label = QLabel(f"Last Name{red_asterisk}")
        self.last_name_label.setContentsMargins(10,0,0,0)
        self.last_name = QLineEdit()
        self.last_name.setFixedWidth(250)
        self.last_name.setFixedHeight(28)
        self.last_name.setContentsMargins(10,0,0,0)
        self.last_name.setValidator(QRegularExpressionValidator(characters_only, self))

        self.phone_no_label = QLabel(f"Phone No.{red_asterisk}")
        self.phone_no_label.setContentsMargins(10,0,0,0)
        self.phone_no = QLineEdit()
        self.phone_no.setFixedWidth(250)
        self.phone_no.setFixedHeight(28)
        self.phone_no.setContentsMargins(10,0,0,0)
        self.phone_no.setValidator(QRegularExpressionValidator(numbers_only, self))

        self.email_address_label = QLabel(f"Email Address{red_asterisk}")
        self.email_address_label.setContentsMargins(10,0,0,0)
        self.email_address = QLineEdit()
        self.email_address.setFixedWidth(250)
        self.email_address.setFixedHeight(28)
        self.email_address.setContentsMargins(10,0,0,0)

        self.home_address_label = QLabel(f"Home Address{red_asterisk}")
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

        self.weight_laundry_label = QLabel(f"Weight of Laundry (kg){red_asterisk}")
        self.weight_laundry_label.setContentsMargins(10,0,0,0)

        self.weight_laundry = QLineEdit()
        self.weight_laundry.setPlaceholderText("kg")
        self.weight_laundry.setContentsMargins(10,0,0,0)
        self.weight_laundry.setFixedWidth(165)
        self.weight_laundry.setValidator(QRegularExpressionValidator(numbers_only, self))

        self.garment_count_label = QLabel(f"Count of Garments{red_asterisk}")
        self.garment_count = QLineEdit()
        self.garment_count.setPlaceholderText("#")
        self.garment_count.setFixedWidth(135)
        self.garment_count.setValidator(QRegularExpressionValidator(numbers_only, self))

        self.addons_label = QLabel("Add-ons")
        self.addons_label.setContentsMargins(0,0,0,0)

        addons_layout = QHBoxLayout()
        addons_layout.setContentsMargins(0,6,0,6)

        addons_container = QWidget()
        addons_container.setLayout(addons_layout)

        self.addons_option1 = QCheckBox("Fabric Softener")
        self.addons_option2 = QCheckBox("Bleach")
        self.addons_option3 = QCheckBox("Baking Soda")
        self.addons_option4 = QCheckBox("Extra Spin") 

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

        self.schedule_buttons = QButtonGroup(self)
        self.schedule_buttons.setExclusive(True)

        self.schedule_label = QLabel("Schedule Pick-Up/Delivery")
        self.priority_btn = QPushButton("Priority\n15~60mins")
        self.priority_btn.setContentsMargins(10,0,0,0)

        self.priority_btn = QPushButton("Priority\n15~60 mins")
        self.priority_btn.setContentsMargins(10,0,0,0)
        self.priority_btn.setCheckable(True)
        self.priority_btn.setChecked(True)
        self.same_day_btn = QPushButton("Same-Day\n~24 hours")
        self.same_day_btn.setContentsMargins(10,0,0,0)
        self.same_day_btn.setCheckable(True)
        self.standard_btn = QPushButton("Standard\n24~ hours")
        self.standard_btn.setContentsMargins(10,0,0,0)
        self.standard_btn.setCheckable(True)

        self.schedule_buttons.addButton(self.priority_btn)
        self.schedule_buttons.addButton(self.same_day_btn)
        self.schedule_buttons.addButton(self.standard_btn)
        self.selected_schedule = None #NEW
        self.schedule_buttons.buttonClicked.connect(self.on_schedule_selected) #NEW

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

        confirmation_layout = QVBoxLayout()
        confirmation_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        confirmation_container = QWidget()
        confirmation_container.setLayout(confirmation_layout)

        self.confirmation_container = Confirmation()
        confirmation_layout.addWidget(self.confirmation_container)

        success_layout = QVBoxLayout()
        success_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        success_layout.setContentsMargins(0, 10, 0, 0)
        success_container = QWidget()
        success_container.setLayout(success_layout)

        self.success_container = successScreen(main_window=self.main_window)
        success_layout.addWidget(self.success_container)
        
        self.stepbystep_forms.addWidget(confirmation_container)
        self.stepbystep_forms.addWidget(success_container)

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

    def on_schedule_selected(self, button): #NEW
        name, _, time = button.text().partition("\n") #NEW
        self.selected_schedule = (name, time) #NEW

    def collect_data(self): #NEW
        schedule_btn = self.schedule_buttons.checkedButton() #NEW
        schedule_name, _, schedule_time = schedule_btn.text().partition("\n") #NEW

        addon_buttons = (self.addons_option1, self.addons_option2, self.addons_option3, self.addons_option4) #NEW
        service_buttons = (self.services_option1, self.services_option2, self.services_option3) #NEW
        service = next(b.text() for b in service_buttons if b.isChecked()) #NEW

        return {
            "first_name": self.first_name.text().strip(), "last_name": self.last_name.text().strip(), #NEW
            "phone_no": self.phone_no.text().strip(), "email_address": self.email_address.text().strip(), #NEW
            "home_address": self.home_address.text().strip(), "service": service.replace("&&", "&"), #NEW
            "addons": [b.text() for b in addon_buttons if b.isChecked()], #NEW
            "weight_kg": self.weight_laundry.text().strip(), #NEW
            "garment_count": self.garment_count.text().strip(), #NEW
            "note": self.laundry_note.text().strip(), #NEW
            "schedule": schedule_name, "schedule_time": schedule_time #NEW
        }

    def validate(self): #NEW
        required_info = [
            self.first_name, self.last_name, self.phone_no, self.email_address,
            self.home_address, self.weight_laundry, self.garment_count
        ]
        if any(not information.text().strip() for information in required_info):
            return "All required fields must be filled."
        if self.schedule_buttons.checkedButton() is None: #NEW
            return "Please select a Pick-Up/Delivery schedule." #NEW
        try: #NEW
            float(self.weight_laundry.text()) #NEW
            int(self.garment_count.text()) #NEW
        except ValueError: #NEW
            return "Weight must be a number and garment count must be a whole number." #NEW
        return None #NEW

    def next_step(self):
        if self.form_count == 0:
            error = self.validate() #NEW
            if error: #NEW
                QMessageBox.warning(self, 'Warning', error) #NEW
                return #NEW
            self.appointment_data = self.collect_data() #NEW
            self.confirm_appointment_data()

        elif self.form_count == 1:
            self.save_appointment_data()
            self.appointment_saved.emit(self.appointment_data) #NEW
        else: #NEW
            return #NEW

        self.progress_bar.confirm_step()
        self.form_count +=1
        self.stepbystep_forms.setCurrentIndex(self.form_count)

        if self.form_count == 2:
            self.confirm_btn.setVisible(False)
            transparent_png_path = os.path.join(base_dir, "assets", "Btn icons", "transparent.png")
            self.back_btn.setIcon(QIcon(transparent_png_path))
            self.back_btn.setIconSize(QSize(40, 40))
            self.back_btn.setFlat(True)
            self.back_btn.setEnabled(False)
            self.back_btn.setToolTip("")

    def closeEvent(self, event): #NEW
        if self.main_window: #NEW
            self.main_window.show() #NEW
        super().closeEvent(event) #NEW

    def close_appointment_window(self):

        if self.form_count == 1:
            self.progress_bar.previous_step()
            self.form_count -= 1
            self.stepbystep_forms.setCurrentIndex(self.form_count)
        else:

         if self.main_window:
            self.main_window.show()
         self.close()

    def confirm_appointment_data(self):

            first_name = self.first_name.text().strip()
            last_name = self.last_name.text().strip()

            service = "Wash-and-Fold" # just the default setting 
            if self.services_option1.isChecked():
             service = "Wash-and-Fold"
            elif self.services_option2.isChecked():
                service = "Dry-Cleaning"
            elif self.services_option3.isChecked():
                service = "Pressing & Ironing"

            addons = []
            if self.addons_option1.isChecked():
                addons.append("Fabric Softener")
            if self.addons_option2.isChecked():
                addons.append("Bleach")
            if self.addons_option3.isChecked():
                addons.append("Baking Soda")
            if self.addons_option4.isChecked():
                addons.append("Extra Spin")

            list_addons =", ".join(addons) if addons else "None"

            weight_laundry = self.weight_laundry.text().strip()
            garment_count = self.garment_count.text().strip()
            laundry_note = self.laundry_note.text().strip() or "None"

            schedule_delivery = "None Selected"
            if self.priority_btn.isChecked():
                schedule_delivery = "Priority: 15-60 mins"
            elif self.same_day_btn.isChecked():
                schedule_delivery = "Same Day: ~24 hours"
            elif self.standard_btn.isChecked():
                schedule_delivery = "Standard: 24~ hours"

            self.confirmation_container.name.setText(f"{first_name} {last_name}")
            self.confirmation_container.delivery_option.setText(schedule_delivery)
            self.confirmation_container.ls_options_label.setText(f"Service: {service}")
            self.confirmation_container.ls_options_label2.setText(f"Weight of Laundry: {weight_laundry}kg")
            self.confirmation_container.ls_options_label3.setText(f"Count of Garments: {garment_count} garment(s)")
            self.confirmation_container.ls_options_label4.setText(f"Add-ons: {list_addons}")
            self.confirmation_container.ls_options_label5.setText(f"Note/Additional Requests: {laundry_note}")

    def save_appointment_data(self):
        try:

            data_dir = base_dir / "data"
            data_dir.mkdir(parents=True, exist_ok=True) #NEW

            current = QDateTime.currentDateTime()
            timestamp = current.toString("hh-mm-ss_AP")
            date = current.toString("MM-dd-yyyy")

            first_name = self.first_name.text().strip()
            last_name = self.last_name.text().strip()
            phone_no = self.phone_no.text().strip()
            email_address = self.email_address.text().strip()
            home_address = self.home_address.text().strip()

            if not first_name or not last_name:
                return

            service = "Wash-and-Fold" # just the default setting 
            if self.services_option1.isChecked():
                service = "Wash-and-Fold"
            elif self.services_option2.isChecked():
                service = "Dry-Cleaning"
            elif self.services_option3.isChecked():
                service = "Pressing & Ironing"

            addons = []
            if self.addons_option1.isChecked():
                addons.append("Fabric Softener")
            if self.addons_option2.isChecked():
                addons.append("Bleach")
            if self.addons_option3.isChecked():
                addons.append("Baking Soda")
            if self.addons_option4.isChecked():
                addons.append("Extra Spin")

            list_addons =", ".join(addons) if addons else "None"

            weight_laundry = self.weight_laundry.text().strip()
            garment_count = self.garment_count.text().strip()
            laundry_note = self.laundry_note.text().strip() or "None"

            schedule_delivery = "None Selected"
            if self.priority_btn.isChecked():
                schedule_delivery = "Priority: 15-60 mins"
            elif self.same_day_btn.isChecked():
                schedule_delivery = "Same Day: ~24 hours"
            elif self.standard_btn.isChecked():
                schedule_delivery = "Standard: 24~ hours"

            content = (
                f"Date of Appointment: {date}   Time: {timestamp}\n\n"  
                f"First Name: {first_name}\n"
                f"Last Name: {last_name}\n"
                f"Phone No.: {phone_no}\n"
                f"Email Address: {email_address}\n"
                f"Home Address: {home_address}\n"
                f"Service: {service}\n\n"

                "Laundry Specifications:\n" 
                f"Weight of Laundry (kg): {weight_laundry}kg\n"
                f"Count of Garments: {garment_count} garment(s)\n" 
                f"Add-ons: {list_addons}\n"
                f"Note/Additional Requests: {laundry_note}\n"

                f"Schedule Pick-up/Delivery: {schedule_delivery}\n" 
            )

            filename = f"Appointment_{last_name}_{date}_{timestamp}.txt"
            full_path = os.path.join(data_dir, filename)

            with open(full_path, "w") as file:
                file.write(content)

        except Exception as e:
            print(f"Auto-save failed: {e}")

#======= signals and event calls ======== end

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = addAppointment()
    window.show()
    sys.exit(app.exec())
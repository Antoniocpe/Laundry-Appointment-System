import sys, json, tempfile #NEW
from pathlib import Path
from PyQt6.QtCore import Qt, QPointF #NEW
from PyQt6.QtGui import QPainter, QPixmap, QPolygonF, QColor #NEW
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QGridLayout, QPushButton,
                             QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget, 
                             QMessageBox, QComboBox) #NEW

base_dir = Path(__file__).resolve().parent.parent 
if str(base_dir) not in sys.path: 
    sys.path.insert(0, str(base_dir))  
    
from widget.Washer_button import CustomerCard
from UI.addAppointment import addAppointment


# The idea of this line is to save appointments even the app exits
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "appointments.json" #NEW

MAX_WASHERS = 4

# key stored in the json, text in the dropdown, status-light colour
STATUSES = [ 
    ("pending",  "Pending",     "#e5484d"), #NEW
    ("progress", "In Progress", "#f5b942"), #NEW
    ("pickup",   "For Pick-up", "#6fd36f"), #NEW
    
] 
STATUS_COLOR = {key: color for key, _, color in STATUSES} #NEW
DEFAULT_STATUS = "pending" #NEW

DETAIL_SECTIONS = [ #NEW
    ("Personal Information",[("Name:", "name", False),("Contact Number:", "phone_no", False)]), #NEW
    ("Laundry Details",[("Weight (kg):", "weight_kg", False),("# of Garments:", "garment_count", False), #NEW
                        ("Add-ons:", "addons", False)]), #NEW
    ("Delivery",[(None, "schedule", False)]), #NEW
    ("Transaction Details",[("Service Fee:", "service_fee", True),("Add-ons Fee:", "addons_fee", True)]), #NEW
] 


def make_arrow_image(): #NEW
    """Draws the white dropdown triangle once and returns its file path for the QSS.""" #NEW
    path = Path(tempfile.gettempdir()) / "laundry_arrow_down.png" #NEW
    pm = QPixmap(14, 9) #NEW
    pm.fill(Qt.GlobalColor.transparent) #NEW
    p = QPainter(pm) #NEW
    p.setRenderHint(QPainter.RenderHint.Antialiasing) #NEW
    p.setPen(Qt.PenStyle.NoPen) #NEW
    p.setBrush(QColor("#ffffff")) #NEW
    p.drawPolygon(QPolygonF([QPointF(0, 0), QPointF(14, 0), QPointF(7, 9)])) #NEW
    p.end() #NEW
    pm.save(str(path)) #NEW
    return path.as_posix() #NEW


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("Dashboard_style")
        self.appointments = []  #NEW
        self.slots = []  #NEW
        self.selected = None  #NEW

        # ----- widgets -----
        self.header = QLabel("DASHBOARD") #NEW
        self.add_appointment_btn = QPushButton("+  Add Appointment") #NEW
        self.add_appointment_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_appointment_btn.setFixedSize(190, 32) #NEW
        self.add_appointment_btn.clicked.connect(self.open_appointment_window)

        self.inQueue_text = QLabel("Washes In Queue")
        self.total_text = QLabel(f"In total: 0 / {MAX_WASHERS}") #NEW

        self.details_placeholder = QLabel("Select a washer to view details")
        self.details_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.customers_layout = QGridLayout() #NEW
        self.customers_layout.setContentsMargins(14, 14, 14, 14) #NEW
        self.customers_layout.setSpacing(10) #NEW
        for col in range(2): #NEW
            self.customers_layout.setColumnStretch(col, 1) #NEW
        for row in range((MAX_WASHERS + 1) // 2): #NEW
            self.customers_layout.setRowStretch(row, 1) #NEW

        washers_panel = QFrame() 
        washers_panel.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True) 
        washers_panel.setLayout(self.customers_layout) #NEW

        for i in range(MAX_WASHERS): #NEW
            card = CustomerCard()      # starts as UNOCCUPIED 
            card.clicked.connect(self.select_customer) #NEW
            self.slots.append(card) #NEW
            self.customers_layout.addWidget(card, i // 2, i % 2) #NEW

        # ----- middle -----
        header_layout = QHBoxLayout() #NEW
        header_layout.addWidget(self.header) #NEW
        header_layout.addStretch() #NEW
        header_layout.addWidget(self.add_appointment_btn, alignment=Qt.AlignmentFlag.AlignVCenter) #NEW

        washers_info = QVBoxLayout() #NEW
        washers_info.setSpacing(0) #NEW
        washers_info.addWidget(self.inQueue_text) #NEW
        washers_info.addWidget(self.total_text) #NEW

        middle_layout = QVBoxLayout()
        middle_layout.setContentsMargins(30, 16, 22, 22) #NEW
        middle_layout.setSpacing(8) #NEW
        middle_layout.addLayout(header_layout)
        middle_layout.addLayout(washers_info)
        middle_layout.addWidget(washers_panel, stretch=1) #NEW

        # ----- details (right) -----
        details_container = QFrame() 
        details_container.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # page 0 = "select a washer", page 1 = the customer's details #NEW
        self.details_stack = QStackedWidget()#NEW 
        self.details_stack.addWidget(self.details_placeholder)#NEW 
        self.details_stack.addWidget(self.build_details_page())#NEW 
        
        details_layout = QVBoxLayout(details_container)
        details_layout.setContentsMargins(16, 16, 16, 12) #NEW
        details_layout.addWidget(self.details_stack) #NEW 

        # ----- page layout -----
        page_layout = QHBoxLayout(self)
        page_layout.addLayout(middle_layout, stretch=2)
        page_layout.addWidget(details_container, stretch=1)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(0) #NEW

        # ----- object names (used by the QSS) -----
        self.header.setObjectName("header")
        self.add_appointment_btn.setObjectName("addApptBtn")
        self.inQueue_text.setObjectName("inQueue_text")
        self.total_text.setObjectName("total_text")
        washers_panel.setObjectName("washers_panel") #NEW
        details_container.setObjectName("details_layout")
        self.details_stack.setObjectName("details_stack") #NEW
        self.details_placeholder.setObjectName("details_placeholder")
        
        self.load_appointments() #NEW 
        if self.appointments: #NEW
            self.select_customer(self.appointments[0]) #NEW
    
    # ------------------------------------------------------------------ #NEW
    # details panel #NEW
    # ------------------------------------------------------------------ #NEW
    def build_details_page(self): #NEW 
        page = QWidget() #NEW
        page.setObjectName("details_page") #NEW
        layout = QVBoxLayout(page) #NEW
        layout.setContentsMargins(0, 0, 0, 0) #NEW
        layout.setSpacing(2) #NEW
        layout.setAlignment(Qt.AlignmentFlag.AlignTop) #NEW
        
        self.details_title = QLabel("") #NEW
        self.details_title.setObjectName("details_title") #NEW
        self.details_title.setAlignment(Qt.AlignmentFlag.AlignRight) #NEW

        self.status_combo = QComboBox() #NEW
        self.status_combo.setObjectName("statusCombo") #NEW
        self.status_combo.setCursor(Qt.CursorShape.PointingHandCursor) #NEW
        self.status_combo.setStyleSheet( #NEW
            f'QComboBox::down-arrow {{ image: url("{make_arrow_image()}"); ' #NEW
            f'width: 14px; height: 9px; }}') #NEW
        for key, text, _ in STATUSES: #NEW
            self.status_combo.addItem(text, key) #NEW
        self.status_combo.currentIndexChanged.connect(self.on_status_changed) #NEW
        self.apply_status_style(DEFAULT_STATUS) #NEW

        layout.addWidget(self.details_title) #NEW
        layout.addSpacing(8) #NEW
        layout.addWidget(self.status_combo) #NEW
        layout.addSpacing(14) #NEW
        
        self.detail_values = {} #NEW
        for section_title, rows in DETAIL_SECTIONS: #NEW
            section = QLabel(section_title) #NEW
            section.setProperty("tag", "sectionTitle") #NEW
            layout.addWidget(section) #NEW
            
            for label_text, key, inline in rows: #NEW
                value = QLabel("-") #NEW
                value.setProperty("tag", "fieldValue") #NEW
                value.setWordWrap(True) #NEW
                value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse) #NEW
                self.detail_values[key] = value #NEW

                if label_text is None:               # value only #NEW
                    layout.addWidget(value) #NEW
                    continue #NEW

                label = QLabel(label_text) #NEW
                label.setProperty("tag", "fieldLabel") #NEW
                if inline:                           # "Service Fee:        100" #NEW
                    row = QHBoxLayout() #NEW
                    row.addWidget(label) #NEW
                    row.addStretch() #NEW
                    row.addWidget(value) #NEW
                    layout.addLayout(row) #NEW
                else:                                # label above value #NEW
                    layout.addWidget(label) #NEW
                    layout.addWidget(value) #NEW
            layout.addSpacing(12) #NEW
            
        layout.addStretch()#NEW
        return page #NEW
    
    def show_details(self, data): #NEW
        name = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip() #NEW
        self.details_title.setText(name.upper()) #NEW

        addons = data.get("addons") or [] #NEW
        if isinstance(addons, str): #NEW
            addons = [addons] #NEW

        schedule = data.get("schedule") #NEW
        if schedule and data.get("schedule_time"): #NEW
            schedule = f"{schedule} ({data['schedule_time']})" #NEW

        view = dict(data) #NEW
        view["name"] = name #NEW
        view["addons"] = "\n".join(f"•  {a}" for a in addons) if addons else "None" #NEW
        view["schedule"] = schedule #NEW
        
        for key, label in self.detail_values.items(): #NEW
            value = view.get(key) #NEW
            label.setText(str(value) if value not in (None, "") else "-") #NEW

        status = data.get("status", DEFAULT_STATUS) #NEW
        self.status_combo.blockSignals(True) #NEW
        self.status_combo.setCurrentIndex(max(0, self.status_combo.findData(status))) #NEW
        self.status_combo.blockSignals(False) #NEW
        self.apply_status_style(status) #NEW
            
        self.details_stack.setCurrentIndex(1) #NEW 
        
    def apply_status_style(self, status): #NEW
        """The dropdown colour is driven by a QSS property.""" #NEW
        self.status_combo.setProperty("status", status) #NEW
        self.status_combo.style().unpolish(self.status_combo) #NEW
        self.status_combo.style().polish(self.status_combo) #NEW

    def on_status_changed(self, index): #NEW
        if self.selected is None: #NEW
            return #NEW
        status = self.status_combo.itemData(index) #NEW
        self.selected["status"] = status #NEW
        self.apply_status_style(status) #NEW

        card = self.card_for(self.selected) #NEW
        if card: #NEW
            card.set_status_color(STATUS_COLOR[status]) #NEW
        self.save_appointments() #NEW

    # ------------------------------------------------------------------ #NEW
    # customers #NEW
    # ------------------------------------------------------------------ #NEW
    def card_for(self, data): #NEW
        return next((c for c in self.slots if c.data is data), None) #NEW

    def add_customer(self, data, save=True): #NEW
        if self.is_full(): #NEW
            return      
        data.setdefault("status", DEFAULT_STATUS) #NEW

        card = self.slots[len(self.appointments)]      # first free washer #NEW
        self.appointments.append(data) #NEW
        
        name = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip() #NEW
        card.set_customer(name, data, STATUS_COLOR.get(data["status"], STATUS_COLOR[DEFAULT_STATUS])) #NEW

        self.update_total() #NEW
        if save:  #NEW
            self.save_appointments()  #NEW
    
    def select_customer(self, data):  #NEW
        if not data:  #NEW
            return #NEW
        self.selected = data #NEW
        for card in self.slots: #NEW
            card.set_selected(card.data is data) #NEW
        self.show_details(data) #NEW
    
    def save_appointments(self):  #NEW
        try: 
            DATA_FILE.parent.mkdir(parents=True, exist_ok=True)  #NEW
            DATA_FILE.write_text(json.dumps(self.appointments, indent=2), encoding="utf-8")#NEW
        except OSError as e:   #NEW
            print(f"Could not save appointments: {e}")  #NEW
            
    def load_appointments(self):  #NEW
        if not DATA_FILE.exists():  #NEW
            return  #NEW
        try:
            text = DATA_FILE.read_text(encoding="utf-8").strip() #NEW
            if not text:             # empty file, nothing to load #NEW
                return #NEW
            for data in json.loads(text): #NEW
                self.add_customer(data, save=False) #NEW
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
            print(f"Could not load appointments: {e}")  #NEW           
    
    def open_appointment_window(self):
        if self.is_full():
            QMessageBox.information(self, "All washers in use", #NEW
                                    f"All {MAX_WASHERS} washers are currently in use.") #NEW
            return
        main_window = self.window()
        self.appointment_window = addAppointment(main_window=main_window)
        self.appointment_window.appointment_saved.connect(self.add_customer)  #NEW
        self.appointment_window.show()

        if main_window:
            main_window.hide()  #NEW     
    
    def is_full(self):  #NEW 
        return len(self.appointments) >= MAX_WASHERS #NEW

    def update_total(self): #NEW 
        self.total_text.setText(f"In total: {len(self.appointments)} / {MAX_WASHERS}") #NEW

        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    base_dir = Path(__file__).resolve().parent.parent
    dashboard_qss = base_dir / "styles" / "Dashboard_style.qss"

    if dashboard_qss.exists():
        app.setStyleSheet(dashboard_qss.read_text())

    window = Dashboard()
    window.show()
    sys.exit(app.exec())

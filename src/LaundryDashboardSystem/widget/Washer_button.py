import sys
from PyQt6.QtCore import Qt, QRectF, QSize, pyqtSignal 
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QFrame, 
                            QGridLayout, QHBoxLayout)
from PyQt6.QtGui import QPainter, QPen, QColor, QPalette

from pathlib import Path

EMPTY_DOT_COLOR = "#8c8c8c" #NEW

# The idea of this function is to show the status of a washer
class StatusDot(QWidget):
    def __init__(self, color="#6fd36f", size=22): 
        super().__init__()
        self._color = QColor(color)
        self.setFixedSize(size, size)

    def set_color(self, color):
        self._color = QColor(color)
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QPen(self._color.darker(115), 2))
        p.setBrush(self._color)
        p.drawEllipse(QRectF(self.rect()).adjusted(2, 2, -2, -2))


class WasherWidget(QWidget):
    #The big circle of the washer Icon thick gray ring + light cyan fill + black when unoccupied
    FILL = "#b8f2ff" #NEW
    FILL_HOVER = "#e0f8ff" #NEW
    FILL_EMPTY = "#2b2b2b" #NEW

    def __init__(self, ring="#c8cfd8", ring_width=14): #NEW
        super().__init__()
        self._ring = QColor(ring)
        self._w = ring_width
        self._occupied = False #NEW
        self._hover = False #NEW
        self.setMinimumSize(110, 110) #NEW

    def sizeHint(self):
        return QSize(170, 170) #NEW

    def set_occupied(self, occupied): #NEW
        self._occupied = occupied #NEW
        self._hover = False #NEW
        self.update() #NEW

    def set_hover(self, hover): #NEW
        if self._occupied: #NEW
            self._hover = hover #NEW
            self.update() #NEW

    def _fill_color(self): #NEW
        if not self._occupied: #NEW
            return QColor(self.FILL_EMPTY) #NEW
        return QColor(self.FILL_HOVER if self._hover else self.FILL) #NEW

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QPen(self._ring, self._w))
        p.setBrush(self._fill_color()) #NEW
        # largest centered square, inset by half the pen so the ring isn't clipped
        side = min(self.width(), self.height()) - self._w
        x = (self.width() - side) / 2
        y = (self.height() - side) / 2
        p.drawEllipse(QRectF(x, y, side, side))


class CustomerCard(QWidget):
    """One washer slot. data=None -> 'UNOCCUPIED' card; otherwise a customer.""" #NEW
    clicked = pyqtSignal(object) #NEW

    def __init__(self, name="", data=None, status_color="#6fd36f"): #NEW
        super().__init__()

        self.data = None #NEW
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True) #NEW
        self.setObjectName("customerCard")  #NEW
        self.setProperty("selected", False) #NEW
        
        # --- widgets ---
        self.status = StatusDot()
        self.status.setObjectName("statusDot")

        self.name = QLabel() #NEW
        self.name.setAlignment(Qt.AlignmentFlag.AlignCenter) #NEW
        self.name.setObjectName("customer_name")

        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.NoFrame) #NEW
        self.line.setFixedHeight(2) #NEW
        self.line.setObjectName("cardLine")

        self.washer = WasherWidget()

        # --- layout: 3 rows x 2 columns ---
        #   row 0:  [status] [        name        ]
        #   row 1:  [------------ line -----------]
        #   row 2:  [----------- washer ----------]
        layout = QGridLayout(self) #NEW
        layout.setContentsMargins(10, 8, 10, 8) #NEW
        layout.setVerticalSpacing(4) #NEW
        layout.addWidget(self.status, 0, 0) #NEW
        layout.addWidget(self.name, 0, 1) #NEW
        layout.addWidget(self.line, 1, 0, 1, 2) #NEW
        layout.addWidget(self.washer, 2, 0, 1, 2) #NEW
        layout.setColumnStretch(1, 1) #NEW
        layout.setRowStretch(2, 1) #NEW
        
        self.set_customer(name, data, status_color) #NEW

    # ---- state ---- #NEW
    @property #NEW
    def occupied(self): #NEW
        return self.data is not None #NEW

    def set_customer(self, name, data, status_color="#6fd36f"): #NEW
        self.data = data #NEW
        if self.occupied: #NEW
            self.name.setText(name.upper()) #NEW
            self.status.set_color(status_color) #NEW
            self.setCursor(Qt.CursorShape.PointingHandCursor) #NEW
        else: #NEW
            self.name.setText("UNOCCUPIED") #NEW
            self.status.set_color(EMPTY_DOT_COLOR) #NEW
            self.setCursor(Qt.CursorShape.ArrowCursor) #NEW
        self.washer.set_occupied(self.occupied) #NEW

    def set_status_color(self, color): #NEW
        if self.occupied: #NEW
            self.status.set_color(color) #NEW

    def set_selected(self, selected):  #NEW
        self.setProperty("selected", selected) #NEW
        self.style().unpolish(self) #NEW
        self.style().polish(self) #NEW
 
    # ---- events ---- #NEW
    def enterEvent(self, event): #NEW
        self.washer.set_hover(True) #NEW
        super().enterEvent(event) #NEW

    def leaveEvent(self, event): #NEW
        self.washer.set_hover(False) #NEW
        super().leaveEvent(event) #NEW

    def mousePressEvent(self, event):  #NEW
        if self.occupied and event.button() == Qt.MouseButton.LeftButton: #NEW
            self.clicked.emit(self.data) #NEW
        super().mousePressEvent(event) #NEW
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Washer_qss = Path(__file__).resolve().parent.parent / "styles" / "Dashboard_style.qss" #NEW
    if Washer_qss.exists(): #NEW
        app.setStyleSheet(Washer_qss.read_text())

    holder = QWidget() #NEW
    row = QHBoxLayout(holder) #NEW
    row.addWidget(CustomerCard("Customer #1", {"first_name": "Customer"})) #NEW
    row.addWidget(CustomerCard())          
    holder.resize(520, 280) #NEW
    holder.show() #NEW
    sys.exit(app.exec())
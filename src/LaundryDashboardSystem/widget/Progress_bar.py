import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPen, QBrush, QFont, QColor
from PyQt6.QtCore import Qt, QRect

class ProgressBar(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(800,80) 

        self.step_count = 0
        self.circle_color1 = QColor("#6491bf")
        self.circle_color2 = QColor("#a8a8a8")
        self.circle_color3 = QColor("#a8a8a8")
        
    def confirm_step(self):
        self.step_count +=1

        if self.step_count == 1:
            self.circle_color2 = QColor("#6491bf")
            self.update()
        elif self.step_count == 2:
            self.circle_color3 = QColor("#6491bf")
            self.update()
        else:
            pass

    def previous_step(self):
        if self.step_count == 1:
            self.circle_color2 = QColor("#a8a8a8")
            self.circle_color3 = QColor("#a8a8a8")
            self.step_count -= 1
            self.update()
        else:
            pass
        
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        font = QFont("Arial", 16, 700)
        font2 = QFont("Arial", 11)
        painter.setPen(QPen(self.circle_color1, 2, Qt.PenStyle.SolidLine))
        #painter.setBrush(QBrush(QColor("#6491bf"), Qt.BrushStyle.SolidPattern))
        painter.setBrush(QBrush(self.circle_color1, Qt.BrushStyle.SolidPattern))

        rect = QRect(130,5,50,50)
        painter.drawEllipse(rect)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.white)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "1")

        text = QRect(80,40,150,50)
        painter.setPen(Qt.GlobalColor.black)
        painter.setFont(font2)
        painter.drawText(text, Qt.AlignmentFlag.AlignCenter, "Booking Details")

        painter.setPen(QPen(self.circle_color2, 2, Qt.PenStyle.SolidLine))
        painter.drawLine(190, 30, 350, 30)

        painter.setPen(QPen(self.circle_color2, 2, Qt.PenStyle.SolidLine))
        #painter.setBrush(QBrush(QColor("#a8a8a8"), Qt.BrushStyle.SolidPattern))
        painter.setBrush(QBrush(self.circle_color2, Qt.BrushStyle.SolidPattern))
        
        rect = QRect(370,5,50,50)
        painter.drawEllipse(rect)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.white)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "2")

        text = QRect(320,40,150,50)
        painter.setPen(Qt.GlobalColor.black)
        painter.setFont(font2)
        painter.drawText(text, Qt.AlignmentFlag.AlignCenter, "Confirmation")

        painter.setPen(QPen(self.circle_color3, 2, Qt.PenStyle.SolidLine))
        painter.drawLine(430, 30, 590, 30)

        painter.setPen(QPen(self.circle_color3, 2, Qt.PenStyle.SolidLine))
        #painter.setBrush(QBrush(QColor("#a8a8a8"), Qt.BrushStyle.SolidPattern))
        painter.setBrush(QBrush(self.circle_color3, Qt.BrushStyle.SolidPattern))

        rect = QRect(610,5,50,50)
        painter.drawEllipse(rect)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.white)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "3")

        text = QRect(560,40,150,50)
        painter.setPen(Qt.GlobalColor.black)
        painter.setFont(font2)
        painter.drawText(text, Qt.AlignmentFlag.AlignCenter, "Success")

        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProgressBar()
    window.show()
    sys.exit(app.exec())


        
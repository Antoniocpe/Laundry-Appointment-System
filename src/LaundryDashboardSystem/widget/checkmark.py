import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPen, QBrush, QFont, QColor
from PyQt6.QtCore import Qt, QRect

class Checkmark(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(250, 260) 
 
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        font = QFont("Arial", 12, 700)
        painter.setPen(QPen(QColor("#b6c9e0"), 2, Qt.PenStyle.SolidLine))
        #painter.setBrush(QBrush(QColor("#6491bf"), Qt.BrushStyle.SolidPattern))
        painter.setBrush(QBrush(QColor("#b6c9e0"), Qt.BrushStyle.SolidPattern))

        rect = QRect(10, 10, 230, 230)
        painter.drawEllipse(rect)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.white)

        painter.setPen(QPen(QColor("#6491bf"), 2, Qt.PenStyle.SolidLine))
        #painter.setBrush(QBrush(QColor("#a8a8a8"), Qt.BrushStyle.SolidPattern))
        painter.setBrush(QBrush(QColor("#6491bf"), Qt.BrushStyle.SolidPattern))

        rect = QRect(35, 35, 180, 180)
        painter.drawEllipse(rect)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.white)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "[insert icon here]")

        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Checkmark()
    window.show()
    sys.exit(app.exec())


        
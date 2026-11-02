import sys, os
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPen, QBrush, QFont, QColor, QImage
from PyQt6.QtCore import Qt, QRect
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

class Checkmark(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(245, 245) 
 
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        checkmark = QImage(os.path.join(base_dir, "assets", "Btn icons", "checkmark.png"))
        self.image = checkmark.scaled(320, 320, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)                                     


        font = QFont("Arial", 12, 700)
        painter.setPen(QPen(QColor("#b6c9e0"), 2, Qt.PenStyle.SolidLine))
        #painter.setBrush(QBrush(QColor("#6491bf"), Qt.BrushStyle.SolidPattern))
        painter.setBrush(QBrush(QColor("#b6c9e0"), Qt.BrushStyle.SolidPattern))

        rect = QRect(8, 10, 230, 230)
        painter.drawEllipse(rect)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.white)

        painter.setPen(QPen(QColor("#6491bf"), 2, Qt.PenStyle.SolidLine))
        #painter.setBrush(QBrush(QColor("#a8a8a8"), Qt.BrushStyle.SolidPattern))
        painter.setBrush(QBrush(QColor("#6491bf"), Qt.BrushStyle.SolidPattern))

        rect = QRect(33, 35, 180, 180)
        painter.drawEllipse(rect)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.white)
        painter.drawImage(-41, -30, self.image)

        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Checkmark()
    window.show()
    sys.exit(app.exec())


        
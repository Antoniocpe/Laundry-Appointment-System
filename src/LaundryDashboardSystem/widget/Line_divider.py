import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPen, QBrush, QFont, QColor
from PyQt6.QtCore import Qt, QRect

class Line_divider_thingy(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(550,8) 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        painter.setPen(QPen(QColor("#a8a8a8"), 2, Qt.PenStyle.SolidLine))
        painter.drawLine(20, 2, 515, 2)

        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Line_divider_thingy()
    window.show()
    sys.exit(app.exec())


        
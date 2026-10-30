import sys, os
from functools import partial
from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                             QHBoxLayout, QFrame, QStackedWidget)

from Dashboard import Dashboard
from Transaction import Transaction
from About import About


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Laundry Dashboard System")
        self.setFixedSize(800, 527)
        self.setObjectName("mainWindow")
        # lets the QSS background rule paint on a plain QWidget
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # ===== Pages =====
        self.dashboard_page = Dashboard()
        self.transaction_page = Transaction()
        self.about_page = About()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.dashboard_page)     # index 0
        self.stack.addWidget(self.transaction_page)   # index 1
        self.stack.addWidget(self.about_page)         # index 2

        # ===== Sidebar buttons =====
        self.dashboard_btn = self.make_sidebar_button("1.png", "Dashboard", "dashboard_btn")
        self.transaction_btn = self.make_sidebar_button("2.png", "Transaction History", "transaction_btn")
        self.about_btn = self.make_sidebar_button("3.png", "About", "about_btn")
        self.exit_btn = self.make_sidebar_button("4.png", "Exit", "exit_btn")

        self.sidebar_buttons = [self.dashboard_btn, self.transaction_btn, self.about_btn]

        for index, b in enumerate(self.sidebar_buttons):
            b.setCheckable(True)
            b.clicked.connect(partial(self.show_page, index))

        self.exit_btn.clicked.connect(self.close)   # not checkable, never keeps a line

        self.dashboard_btn.setChecked(True)         # start on the dashboard

        # ===== Layout =====
        sidebar_layout = QVBoxLayout()
        for b in self.sidebar_buttons + [self.exit_btn]:
            sidebar_layout.addWidget(b)

        sidebar_container = QFrame()
        sidebar_container.setLayout(sidebar_layout)
        sidebar_container.setObjectName("sidebar_layout")

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(sidebar_container, stretch=0)
        main_layout.addWidget(self.stack, stretch=1)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.setObjectName("mainWindow")

    def make_sidebar_button(self, icon_file, tooltip, object_name):
        btn = QPushButton()
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setIcon(QIcon(os.path.join(BASE_DIR, "Btn icons", icon_file)))
        btn.setIconSize(QSize(60, 60))
        btn.setToolTip(tooltip)
        btn.setObjectName(object_name)
        self.set_style_property(btn, "SidebarBtnClass", "sidebar-buttons")
        return btn

    def set_style_property(self, widget, name, value):
        widget.setProperty(name, value)
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def show_page(self, index, *_):
        self.stack.setCurrentIndex(index)
        # keep exactly one page button checked (the clicked one stays checked)
        for i, b in enumerate(self.sidebar_buttons):
            b.setChecked(i == index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_qss = Path(__file__).with_name("main_style.qss")
    dashboard_qss = Path(__file__).with_name("Dashboard_style.qss")

    app.setStyleSheet(
        main_qss.read_text() + "\n" + dashboard_qss.read_text()
    )

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
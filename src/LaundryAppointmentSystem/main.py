import sys, os
from functools import partial
from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                             QHBoxLayout, QFrame, QStackedWidget)

from UI.Dashboard import Dashboard
from UI.Transaction import Transaction
from UI.About import About


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

        current_file_path = Path(__file__).resolve()
        root_dir = current_file_path.parent
        while root_dir.parent != root_dir and root_dir.name != "LaundryDashboardSystem":
            root_dir = root_dir.parent

        assets_dir = root_dir / "assets" / "Btn icons"
        icon_path = assets_dir / icon_file

        # 3. Apply icon safely if found
        if icon_path.exists():
            btn.setIcon(QIcon(str(icon_path)))

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

    # 1. Establish the directory where main.py resides
    base_dir = Path(__file__).resolve().parent

    # 2. Point directly to your styles folder
    # main_style.qss is right next to main.py
    main_qss = base_dir / "main_style.qss"

    # Dashboard_style.qss is inside the styles folder
    dashboard_qss = base_dir / "styles" / "Dashboard_style.qss"

    # 3. Read and apply the stylesheets safely
    style_sheets = []

    if main_qss.exists():
        style_sheets.append(main_qss.read_text())
    else:
        print(f"Warning: Could not find main style at {main_qss}")

    if dashboard_qss.exists():
        style_sheets.append(dashboard_qss.read_text())
    else:
        print(f"Warning: Could not find dashboard style at {dashboard_qss}")

    # Apply the combined styles to the app
    app.setStyleSheet("\n".join(style_sheets))


    window = MainWindow()
    window.show()
    sys.exit(app.exec())

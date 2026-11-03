import sys
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QColor, QPen, QFont
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFrame, QScrollArea, QFileDialog, QApplication
)


class MemberPhotoLabel(QLabel):
    """Custom Label rendering circular images with click-to-upload support."""
    def __init__(self, member_name, image_path=None, parent=None):
        super().__init__(parent)
        self.member_name = member_name
        self.setFixedSize(90, 90)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(f"Click to upload photo for {self.member_name}")

        if image_path and Path(image_path).exists():
            pix = QPixmap(str(image_path))
            if not pix.isNull():
                self.setPixmap(self.make_circular(pix, 90, 90))
            else:
                self.setPixmap(self.create_placeholder_circle(self.member_name))
        else:
            self.setPixmap(self.create_placeholder_circle(self.member_name))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                f"Select Photo for {self.member_name}",
                "",
                "Image Files (*.png *.jpg *.jpeg *.webp *.bmp)"
            )
            if file_path:
                pix = QPixmap(file_path)
                if not pix.isNull():
                    self.setPixmap(self.make_circular(pix, 90, 90))

    @staticmethod
    def make_circular(pixmap, width=90, height=90):
        scaled = pixmap.scaled(
            width, height,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        x = (scaled.width() - width) // 2
        y = (scaled.height() - height) // 2
        cropped = scaled.copy(x, y, width, height)

        rounded = QPixmap(width, height)
        rounded.fill(Qt.GlobalColor.transparent)
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.addEllipse(0, 0, width, height)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, cropped)
        painter.end()

        return rounded

    @staticmethod
    def create_placeholder_circle(name_str):
        width, height = 90, 90
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setPen(QPen(QColor("#2c4d70"), 3))
        painter.setBrush(QColor("#eef4fb"))
        painter.drawEllipse(3, 3, width - 6, height - 6)

        painter.setPen(QColor("#2c4d70"))
        font = QFont("Segoe UI", 11, QFont.Weight.Bold)
        painter.setFont(font)

        initials = "".join([part[0] for part in name_str.split() if part]).upper()
        if not initials:
            initials = "M"

        painter.drawText(0, 0, width, height, Qt.AlignmentFlag.AlignCenter, initials)
        painter.end()

        return pixmap


class About(QWidget):
    def __init__(self):
        super().__init__()

        team_images = self.get_team_image_files()

        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 12, 15, 12)
        main_layout.setSpacing(10)

        # Header Title
        self.header = QLabel("ABOUT")
        self.header.setObjectName("header")
        self.header.setStyleSheet("font-size: 22px; font-weight: 800; color: #2c4d70; font-family: 'Segoe UI', sans-serif;")
        main_layout.addWidget(self.header)

        # Scroll Area Setup (Scrollbars completely hidden)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                width: 0px;
                height: 0px;
                border: none;
                background: transparent;
            }
        """)

        # Content Widget
        self.content = QWidget()
        self.content.setObjectName("about_content")

        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(0, 0, 10, 0)
        content_layout.setSpacing(12)

        # 1. Application Information Card
        info_card = QFrame()
        info_card.setObjectName("about_card")
        info_card.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        info_card.setStyleSheet("QFrame#about_card { background-color: #ffffff; border-radius: 16px; }")

        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(20, 16, 20, 16)
        info_layout.setSpacing(8)

        app_title = QLabel("Laundry Appointment System")
        app_title.setObjectName("app_title")
        app_title.setStyleSheet("font-size: 17px; font-weight: 800; color: #2c4d70;")

        description = QLabel(
            "The Laundry Appointment System is a desktop application developed to make laundry service "
            "appointments easier to manage. It allows customers to provide their personal details, choose "
            "laundry services, specify their laundry requirements, and select a preferred schedule.\n\n"
            "The system is designed to organize appointment information and help laundry staff keep track "
            "of customer bookings and transactions in one place."
        )
        description.setObjectName("description")
        description.setStyleSheet("font-size: 12px; color: #555555; line-height: 1.4;")
        description.setWordWrap(True)

        info_layout.addWidget(app_title)
        info_layout.addWidget(description)
        content_layout.addWidget(info_card)

        # 2. System Features Card
        features_card = QFrame()
        features_card.setObjectName("about_card")
        features_card.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        features_card.setStyleSheet("QFrame#about_card { background-color: #ffffff; border-radius: 16px; }")

        features_layout = QVBoxLayout(features_card)
        features_layout.setContentsMargins(20, 16, 20, 16)
        features_layout.setSpacing(6)

        features_title = QLabel("System Features")
        features_title.setObjectName("section_title")
        features_title.setStyleSheet("font-size: 15px; font-weight: 800; color: #2c4d70;")

        features = [
            "Customer appointment registration",
            "Laundry service selection",
            "Laundry weight and garment information",
            "Additional laundry requests and add-ons",
            "Priority, same-day, and standard scheduling",
            "Booking confirmation",
            "Transaction records"
        ]

        features_layout.addWidget(features_title)

        for feature in features:
            feature_label = QLabel(f"•  {feature}")
            feature_label.setStyleSheet("font-size: 12px; color: #444444;")
            features_layout.addWidget(feature_label)

        content_layout.addWidget(features_card)

        # 3. Development Team Card
        team_card = QFrame()
        team_card.setObjectName("about_card")
        team_card.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        team_card.setStyleSheet("QFrame#about_card { background-color: #ffffff; border-radius: 16px; }")

        team_card_layout = QVBoxLayout(team_card)
        team_card_layout.setContentsMargins(20, 16, 20, 16)
        team_card_layout.setSpacing(12)

        team_title = QLabel("Development Team")
        team_title.setStyleSheet("font-size: 15px; font-weight: 800; color: #2c4d70;")

        team_description = QLabel("The people behind the development of this application.")
        team_description.setStyleSheet("font-size: 12px; color: #777777;")

        team_card_layout.addWidget(team_title)
        team_card_layout.addWidget(team_description)

        team_grid = QGridLayout()
        team_grid.setHorizontalSpacing(12)
        team_grid.setVerticalSpacing(12)

        members = [
            {"name": "Member 1", "role": "UI Functionality"},
            {"name": "Member 2", "role": "Scrum Leader"},
            {"name": "Member 3", "role": "Quality Assurance"},
            {"name": "Member 4", "role": "GUI Design, UI Functionality"},
            {"name": "Member 5", "role": "GUI Design"},
        ]

        self.member_cards = []

        for index, member in enumerate(members):
            card = QFrame()
            card.setObjectName("member_card")
            card.setStyleSheet("""
                QFrame#member_card {
                    background-color: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 12px;
                }
            """)

            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(10, 10, 10, 10)
            card_layout.setSpacing(4)
            card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            assigned_img = team_images[index] if index < len(team_images) else None

            picture_label = MemberPhotoLabel(
                member_name=member["name"],
                image_path=assigned_img
            )

            name = QLabel(member["name"])
            name.setStyleSheet("font-size: 12px; font-weight: bold; color: #222222;")
            name.setAlignment(Qt.AlignmentFlag.AlignCenter)

            role = QLabel(member["role"])
            role.setStyleSheet("font-size: 11px; color: #666666;")
            role.setAlignment(Qt.AlignmentFlag.AlignCenter)

            card_layout.addWidget(picture_label, alignment=Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(name)
            card_layout.addWidget(role)

            team_grid.addWidget(card, 0, index)

            self.member_cards.append({
                "picture": picture_label,
                "name": name,
                "role": role
            })

        team_card_layout.addLayout(team_grid)
        content_layout.addWidget(team_card)

        # Footer
        tech_label = QLabel("Developed using Python and PyQt6.")
        tech_label.setStyleSheet("font-size: 11px; color: #888888; margin-top: 5px;")
        tech_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(tech_label)

        self.scroll_area.setWidget(self.content)
        main_layout.addWidget(self.scroll_area, stretch=1)

    def get_team_image_files(self):
        current_file = Path(__file__).resolve()
        possible_dirs = [
            current_file.parent.parent / "assets" / "team",
            current_file.parent / "assets" / "team",
            Path.cwd() / "assets" / "team",
            Path.cwd() / "src" / "LaundryDashboardSystem" / "assets" / "team",
        ]

        valid_exts = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
        
        for d in possible_dirs:
            if d.exists() and d.is_dir():
                files = sorted([f for f in d.iterdir() if f.is_file() and f.suffix.lower() in valid_exts])
                if files:
                    return files
        return []


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = About()
    window.resize(740, 520)
    window.show()
    sys.exit(app.exec())

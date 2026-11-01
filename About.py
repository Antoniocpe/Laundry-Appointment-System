import sys
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFrame, QScrollArea, QFileDialog, QApplication
)


class MemberPictureLabel(QLabel):
    """Custom picture holder label supporting click-to-upload and automatic rounded cropping."""
    def __init__(self, default_text="1:1\nPHOTO", parent=None):
        super().__init__(parent)
        self.default_text = default_text
        self.setText(default_text)
        self.setFixedSize(90, 90)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Click to upload member photo")
        self.setObjectName("member_picture")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Member Photo", "", "Image Files (*.png *.jpg *.jpeg *.webp *.bmp)"
            )
            if file_path:
                self.set_photo(file_path)

    def set_photo(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            size = self.size()
            # Aspect ratio scaling & center cropping
            scaled = pixmap.scaled(
                size,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            x = (scaled.width() - size.width()) // 2
            y = (scaled.height() - size.height()) // 2
            cropped = scaled.copy(x, y, size.width(), size.height())

            # Render with rounded corners (12px radius)
            rounded = QPixmap(size)
            rounded.fill(Qt.GlobalColor.transparent)
            painter = QPainter(rounded)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            path = QPainterPath()
            path.addRoundedRect(0, 0, size.width(), size.height(), 12, 12)
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, cropped)
            painter.end()

            self.setPixmap(rounded)
            self.setText("")


class About(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 12, 15, 12)
        main_layout.setSpacing(10)

        # Header Title
        self.header = QLabel("ABOUT")
        self.header.setObjectName("header")
        self.header.setStyleSheet("font-size: 22px; font-weight: 800; color: #2c4d70; font-family: 'Segoe UI', sans-serif;")
        main_layout.addWidget(self.header)

        # Scroll area for content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Scrollable container widget
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

        team_description = QLabel("The people behind the development of this application. (Click photo to upload image)")
        team_description.setStyleSheet("font-size: 12px; color: #777777;")

        team_card_layout.addWidget(team_title)
        team_card_layout.addWidget(team_description)

        team_grid = QGridLayout()
        team_grid.setHorizontalSpacing(12)
        team_grid.setVerticalSpacing(12)

        members = [
            {"name": "Member 1", "role": "Developer"},
            {"name": "Member 2", "role": "Developer"},
            {"name": "Member 3", "role": "Documentation"},
            {"name": "Member 4", "role": "Documentation"},
            {"name": "Member 5", "role": "Developer"},
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

            picture = MemberPictureLabel("CLICK TO\nADD PHOTO")

            name = QLabel(member["name"])
            name.setStyleSheet("font-size: 12px; font-weight: bold; color: #222222;")
            name.setAlignment(Qt.AlignmentFlag.AlignCenter)

            role = QLabel(member["role"])
            role.setStyleSheet("font-size: 11px; color: #666666;")
            role.setAlignment(Qt.AlignmentFlag.AlignCenter)

            card_layout.addWidget(picture, alignment=Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(name)
            card_layout.addWidget(role)

            team_grid.addWidget(card, 0, index)

            self.member_cards.append({
                "picture": picture,
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

    def set_member_photo(self, index, image_path):
        """Programmatically load a member photo into the selected card."""
        if 0 <= index < len(self.member_cards):
            self.member_cards[index]["picture"].set_photo(image_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = About()
    window.resize(740, 520)
    window.show()
    sys.exit(app.exec())
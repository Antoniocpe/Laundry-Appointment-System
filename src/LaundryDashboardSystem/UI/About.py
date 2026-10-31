from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class About(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        # Scrollable content container
        self.content = QWidget()
        self.content.setObjectName("about_content")

        layout = QVBoxLayout(self.content)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(18)

        # Header
        self.header = QLabel("About")
        self.header.setObjectName("header")
        layout.addWidget(self.header)

        # Application information
        info_card = QFrame()
        info_card.setObjectName("about_card")

        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(20, 18, 20, 18)
        info_layout.setSpacing(10)

        app_title = QLabel("Laundry Appointment System")
        app_title.setObjectName("app_title")

        description = QLabel(
            "The Laundry Appointment System is a desktop application "
            "developed to make laundry service appointments easier to "
            "manage. It allows customers to provide their personal details, "
            "choose laundry services, specify their laundry requirements, "
            "and select a preferred schedule.\n\n"
            "The system is designed to organize appointment information "
            "and help laundry staff keep track of customer bookings and "
            "transactions in one place."
        )
        description.setObjectName("description")
        description.setWordWrap(True)

        info_layout.addWidget(app_title)
        info_layout.addWidget(description)

        layout.addWidget(info_card)

        # System features
        features_card = QFrame()
        features_card.setObjectName("about_card")

        features_layout = QVBoxLayout(features_card)
        features_layout.setContentsMargins(20, 18, 20, 18)
        features_layout.setSpacing(10)

        features_title = QLabel("System Features")
        features_title.setObjectName("section_title")

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
            feature_label.setObjectName("feature_text")
            features_layout.addWidget(feature_label)

        layout.addWidget(features_card)

        # Development team
        team_title = QLabel("Development Team")
        team_title.setObjectName("section_title")
        layout.addWidget(team_title)

        team_description = QLabel(
            "The people behind the development of this application."
        )
        team_description.setObjectName("description")
        layout.addWidget(team_description)

        team_layout = QGridLayout()
        team_layout.setHorizontalSpacing(15)
        team_layout.setVerticalSpacing(15)

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

            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(12, 12, 12, 12)
            card_layout.setSpacing(7)
            card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            picture = QLabel("1:1\nPHOTO")
            picture.setObjectName("member_picture")
            picture.setFixedSize(100, 100)
            picture.setAlignment(Qt.AlignmentFlag.AlignCenter)

            name = QLabel(member["name"])
            name.setObjectName("member_name")
            name.setAlignment(Qt.AlignmentFlag.AlignCenter)

            role = QLabel(member["role"])
            role.setObjectName("member_role")
            role.setAlignment(Qt.AlignmentFlag.AlignCenter)

            card_layout.addWidget(
                picture, alignment=Qt.AlignmentFlag.AlignCenter
            )
            card_layout.addWidget(name)
            card_layout.addWidget(role)

            team_layout.addWidget(card, index // 5, index % 5)

            self.member_cards.append({
                "picture": picture,
                "name": name,
                "role": role
            })

        layout.addLayout(team_layout)

        # Footer
        tech_label = QLabel("Developed using Python and PyQt6.")
        tech_label.setObjectName("footer_text")
        tech_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(10)
        layout.addWidget(tech_label)
        layout.addSpacing(10)

        # Enable scrolling
        self.scroll_area.setWidget(self.content)
        main_layout.addWidget(self.scroll_area)

    def set_member_photo(self, index, image_path):
        """Load a member photo into the selected picture holder."""

        if 0 <= index < len(self.member_cards):
            pixmap = QPixmap(image_path)

            if not pixmap.isNull():
                picture = self.member_cards[index]["picture"]

                picture.setPixmap(
                    pixmap.scaled(
                        picture.size(),
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation
                    )
                )
                picture.setText("")

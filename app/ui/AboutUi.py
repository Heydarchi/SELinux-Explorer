from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PyQt5.QtWidgets import QGroupBox, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import Qt
from AppSetting import *


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self._init_widgets()
        self._config_layout()
        self._config_signals()

    def _init_widgets(self):
        self.lbl_app_icon = QLabel()
        self.lbl_app_name = QLabel(APP_NAME)
        self.lbl_app_version = QLabel(APP_VERSION)
        self.lbl_app_author = QLabel(APP_AUTHOR)
        self.lbl_app_author_email = QLabel(AUTHOR_EMAIL)
        self.lbl_app_license = QLabel("License: " + APP_LICENSE)
        self.lbl_app_website = QLabel(
            "<a href=\"" +
            APP_WEBSITE +
            "\">" +
            APP_WEBSITE +
            "</a>")

        self.btn_ok = QPushButton("OK")

        self.lbl_app_icon.setPixmap(QPixmap(APP_ICON_PATH))

        self.lbl_app_name.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.lbl_app_version.setStyleSheet("font-size: 15px; font-weight: bold;")
        self.lbl_app_author.setStyleSheet("font-size: 15px; font-weight: normal")
        self.lbl_app_author_email.setStyleSheet(
            "font-size: 15px; font-weight: normal;")
        self.lbl_app_website.setStyleSheet(
            "font-size: 15px; font-weight: normal;")
        self.lbl_app_license.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.lbl_app_website.setOpenExternalLinks(True)

        self.lbl_app_icon.setMaximumWidth(100)
        self.lbl_app_icon.setMaximumHeight(100)

        self.lbl_app_icon.setAlignment(Qt.AlignCenter)
        self.lbl_app_name.setAlignment(Qt.AlignCenter)
        self.lbl_app_version.setAlignment(Qt.AlignCenter)
        self.lbl_app_author.setAlignment(Qt.AlignCenter)
        self.lbl_app_author_email.setAlignment(Qt.AlignCenter)
        self.lbl_app_license.setAlignment(Qt.AlignCenter)
        self.lbl_app_website.setAlignment(Qt.AlignCenter)

        self.vbox = QVBoxLayout()

        self.group_box = QGroupBox("About")

        self.hbox = QHBoxLayout()

    def _config_layout(self):
        self.vbox.addWidget(self.lbl_app_icon)
        self.vbox.addWidget(self.lbl_app_name)
        self.vbox.addWidget(self.lbl_app_version)
        self.vbox.addWidget(self.lbl_app_license)
        self.vbox.addWidget(QWidget())
        self.vbox.addWidget(QWidget())
        self.vbox.addWidget(self.lbl_app_author)
        self.vbox.addWidget(self.lbl_app_author_email)
        self.vbox.addWidget(QWidget())
        self.vbox.addWidget(QWidget())
        self.vbox.addWidget(self.lbl_app_website)

        self.vbox.setAlignment(Qt.AlignCenter)
        self.group_box.setLayout(self.vbox)
        self.group_box.setAlignment(Qt.AlignCenter)
        self.hbox.addWidget(self.group_box)

        self.setLayout(self.hbox)

        self.setWindowTitle("About")
        self.setWindowIcon(QIcon(APP_ICON_PATH))
        self.set_window_position()

    def _config_signals(self):
        self.btn_ok.clicked.connect(self.close)

    def set_window_position(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

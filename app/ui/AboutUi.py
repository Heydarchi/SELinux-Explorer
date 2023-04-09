from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PyQt5.QtWidgets import QGroupBox, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import Qt
from AppSetting import *


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initWidgets()
        self.configLayout()
        self.configSinals()

    def initWidgets(self):
        self.lblAppIcon = QLabel()
        self.lblAppName = QLabel(APP_NAME)
        self.lblAppVersion = QLabel(APP_VERSION)
        self.lblAppAuthor = QLabel(APP_AUTHOR)
        self.lblAppAuthorEmail = QLabel(AUTHOR_EMAIL)
        self.lblAppLicense = QLabel("License: " + APP_LICENSE)
        self.lblAppWebsite = QLabel(
            "<a href=\"" +
            APP_WEBSITE +
            "\">" +
            APP_WEBSITE +
            "</a>")

        self.btnOk = QPushButton("OK")

        self.lblAppIcon.setPixmap(QPixmap(APP_ICON_PATH))

        self.lblAppName.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.lblAppVersion.setStyleSheet("font-size: 15px; font-weight: bold;")
        self.lblAppAuthor.setStyleSheet("font-size: 15px; font-weight: normal")
        self.lblAppAuthorEmail.setStyleSheet(
            "font-size: 15px; font-weight: normal;")
        self.lblAppWebsite.setStyleSheet(
            "font-size: 15px; font-weight: normal;")
        self.lblAppLicense.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.lblAppWebsite.setOpenExternalLinks(True)

        self.lblAppIcon.setMaximumWidth(100)
        self.lblAppIcon.setMaximumHeight(100)

        self.lblAppIcon.setAlignment(Qt.AlignCenter)
        self.lblAppName.setAlignment(Qt.AlignCenter)
        self.lblAppVersion.setAlignment(Qt.AlignCenter)
        self.lblAppAuthor.setAlignment(Qt.AlignCenter)
        self.lblAppAuthorEmail.setAlignment(Qt.AlignCenter)
        self.lblAppLicense.setAlignment(Qt.AlignCenter)
        self.lblAppWebsite.setAlignment(Qt.AlignCenter)

        self.vbox = QVBoxLayout()

        self.groupBox = QGroupBox("About")

        self.hbox = QHBoxLayout()

    def configLayout(self):
        self.vbox.addWidget(self.lblAppIcon)
        self.vbox.addWidget(self.lblAppName)
        self.vbox.addWidget(self.lblAppVersion)
        self.vbox.addWidget(self.lblAppLicense)
        self.vbox.addWidget(QWidget())
        self.vbox.addWidget(QWidget())
        self.vbox.addWidget(self.lblAppAuthor)
        self.vbox.addWidget(self.lblAppAuthorEmail)
        self.vbox.addWidget(QWidget())
        self.vbox.addWidget(QWidget())
        self.vbox.addWidget(self.lblAppWebsite)

        self.vbox.setAlignment(Qt.AlignCenter)
        self.groupBox.setLayout(self.vbox)
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.hbox.addWidget(self.groupBox)

        self.setLayout(self.hbox)

        self.setWindowTitle("About")
        self.setWindowIcon(QIcon(APP_ICON_PATH))
        self.setWindowPosition()

    def configSinals(self):
        self.btnOk.clicked.connect(self.close)

    def setWindowPosition(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

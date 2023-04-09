from PyQt5.QtWidgets import QMessageBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize


class UiUtility:
    @staticmethod
    def show_message(title, message, icon_type=QMessageBox.Information):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    @staticmethod
    def ask_question(handle, title, message):
        reply = QMessageBox.question(
            handle, title, message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        return True if reply == QMessageBox.Yes else False

    @staticmethod
    def create_button(title, btn_icon, width, height):
        btn = QPushButton(icon=QIcon(btn_icon))
        btn.setToolTip(title)
        btn.setMinimumSize(width, height)
        btn.setIconSize(QSize(width, height))
        return btn

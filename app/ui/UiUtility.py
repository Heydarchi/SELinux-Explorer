from PyQt5.QtWidgets import QMessageBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize


class UiUtility:
      
    @staticmethod
    def showMessage(title, message, iconType = QMessageBox.Information):
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Information)
      msg.setText(message)
      msg.setWindowTitle("Information MessageBox")
      msg.setStandardButtons(QMessageBox.Ok)
      msg.exec_()

    @staticmethod
    def askQuestion(handle, title, message):
       reply = QMessageBox.question(handle, title, message,
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
       return True if reply == QMessageBox.Yes else False

    @staticmethod
    def createButton(title, btnIcon, width, height):
         btn = QPushButton(icon = QIcon(btnIcon))
         btn.setToolTip(title)
         btn.setMinimumSize(width, height)
         btn.setIconSize(QSize(width, height))
         return btn
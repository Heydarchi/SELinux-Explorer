from PyQt5.QtWidgets import QMessageBox

def showMessage(title, message, iconType = QMessageBox.Information):
   msg = QMessageBox()
   msg.setIcon(QMessageBox.Information)
   msg.setText(message)
   msg.setWindowTitle("Information MessageBox")
   msg.setStandardButtons(QMessageBox.Ok)
   msg.exec_()

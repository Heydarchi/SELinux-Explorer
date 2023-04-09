from PyQt5.QtWidgets import QApplication
from ui.MainUi import *
import sys
from MyLogger import MyLogger

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

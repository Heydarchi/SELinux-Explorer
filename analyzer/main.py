
from PyQt5.QtWidgets import QApplication
from ui.MainUi import *
import sys


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
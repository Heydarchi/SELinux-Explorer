
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QFileDialog, QCheckBox, QDesktopWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from AnalyzerLogic import *
from ui.mainUi import *
import sys


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
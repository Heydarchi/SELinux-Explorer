from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import Qt


class DiagramWindow(QWidget):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self._init_variables()
        self._init_widgets()
        self._config_layout()

    def _init_variables(self):
        self.DEFAULT_WIDTH = 1200 * 2
        self.DEFAULT_HEIGHT = 1024 * 2

    def _init_widgets(self):
        self.im = QPixmap(self.file_path)
        self.label = QLabel()
        self.grid = QGridLayout()

    def _config_layout(self):
        self.grid.addWidget(self.label, 1, 1)
        self.setLayout(self.grid)

        self.setMaximumWidth(self.DEFAULT_WIDTH)
        self.setMaximumHeight(self.DEFAULT_HEIGHT)
        self.label.setPixmap(self.im)

        # self.setGeometry(50,50,320,200)
        self.setWindowTitle("Diagram")
        self.set_window_position()

    def set_window_position(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resizeEvent(self, event):
        self.label.setPixmap(
            self.im.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio)
        )

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget,QPushButton


import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SELinux-Explorer")

        self.lblPath = QLabel("Path")
        self.label2 = QLabel("List of paths")

        self.lblSelectedPath = QLabel()
        self.btnBrowse = QPushButton("Browse")
        self.btnAddToList = QPushButton("Add to list")

        self.layoutPath = QHBoxLayout()


        self.layout = QHBoxLayout()

        self.mainLayout = QVBoxLayout()



        self.container = QWidget()

        # Set the central widget of the Window.
        self.setCentralWidget(self.container)

        self.initUI()

    def initUI(self):

        self.lblSelectedPath.setFixedWidth(280)
        self.lblSelectedPath.setWordWrap(True)
        self.btnBrowse.clicked.connect(self.browsePath)
        self.btnAddToList.clicked.connect(self.addSelectedPathToList)


        self.layoutPath.addWidget(self.lblPath)
        self.layoutPath.addWidget(self.lblSelectedPath)
        self.layoutPath.addWidget(self.btnBrowse)
        self.layoutPath.addWidget(self.btnAddToList)

        self.layout.addWidget(self.label2)

        self.mainLayout.addLayout(self.layoutPath)
        self.mainLayout.addLayout(self.layout)

        self.container.setLayout(self.mainLayout)

    def browsePath(self):
        pass

    def addSelectedPathToList(self):
        pass

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()